from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.document import Document
from app.models.quiz import Quiz, Question, QuizAttempt
from app.schemas.quiz import GenerateQuizRequest, SubmitQuizRequest
from app.services.retrieval import retrieve_document_chunks
from app.services.quiz_generator import generate_quiz
from app.utils.auth import get_current_user


router = APIRouter(
    prefix="/api/quiz",
    tags=["Quiz"]
)


# ============================================================
# GENERATE QUIZ
# ============================================================

@router.post("/generate")
def generate_quiz_endpoint(
    request: GenerateQuizRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # --------------------------------------------------------
    # 1. Check that the document belongs to the user
    # --------------------------------------------------------

    document = (
        db.query(Document)
        .filter(
            Document.id == request.document_id,
            Document.user_id == current_user.id
        )
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Selected document was not found or "
                "does not belong to your account."
            )
        )


    # --------------------------------------------------------
    # 2. Retrieve processed PDF chunks
    # --------------------------------------------------------

    chunks = retrieve_document_chunks(
        db=db,
        document_id=request.document_id,
        user_id=current_user.id
    )

    if not chunks:
        raise HTTPException(
            status_code=400,
            detail=(
                "The selected PDF does not contain "
                "processed study material."
            )
        )


    # --------------------------------------------------------
    # 3. Build LLM context
    # --------------------------------------------------------

    context_parts = []

    for chunk in chunks:

        content = chunk["content"][:2000]

        context_parts.append(
            f"""
Page {chunk['page_number']}:

{content}
"""
        )

    context = "\n".join(context_parts)


    # --------------------------------------------------------
    # 4. Generate quiz using LLM
    # --------------------------------------------------------

    try:

        generated_questions = generate_quiz(
            context=context,
            question_count=request.question_count,
            difficulty=request.difficulty
        )

    except Exception as error:

        print(
            "Quiz generation error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to generate the quiz. "
                "Please try again."
            )
        )


    # --------------------------------------------------------
    # 5. Validate generated questions
    # --------------------------------------------------------

    if not generated_questions:

        raise HTTPException(
            status_code=500,
            detail="The AI did not generate any questions."
        )


    # --------------------------------------------------------
    # 6. Create Quiz record
    # --------------------------------------------------------

    try:

        quiz = Quiz(
            user_id=current_user.id,
            document_id=document.id,
            title=f"{document.filename} Quiz",
            difficulty=request.difficulty,
            question_count=len(generated_questions)
        )

        db.add(quiz)

        db.flush()


        # ----------------------------------------------------
        # 7. Save generated questions
        # ----------------------------------------------------

        saved_questions = []

        for item in generated_questions:

            correct_answer = (
                str(
                    item.get(
                        "correct_answer",
                        ""
                    )
                )
                .strip()
                .upper()
            )

            if correct_answer not in [
                "A",
                "B",
                "C",
                "D"
            ]:

                raise ValueError(
                    "Generated question contains "
                    "an invalid correct answer."
                )


            question = Question(
                quiz_id=quiz.id,

                question=str(
                    item["question"]
                ).strip(),

                topic=str(
                    item.get(
                        "topic",
                        "General"
                    )
                ).strip() or "General",

                option_a=str(
                    item["option_a"]
                ).strip(),

                option_b=str(
                    item["option_b"]
                ).strip(),

                option_c=str(
                    item["option_c"]
                ).strip(),

                option_d=str(
                    item["option_d"]
                ).strip(),

                correct_answer=correct_answer,

                explanation=str(
                    item["explanation"]
                ).strip()
            )

            db.add(question)

            saved_questions.append(question)


        # ----------------------------------------------------
        # 8. Commit quiz + questions
        # ----------------------------------------------------

        db.commit()


        # ----------------------------------------------------
        # 9. Refresh records
        # ----------------------------------------------------

        db.refresh(quiz)

        for question in saved_questions:
            db.refresh(question)


    except Exception as error:

        db.rollback()

        print(
            "Quiz database error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to save the generated quiz. "
                "Please try again."
            )
        )


    # --------------------------------------------------------
    # 10. Return generated quiz
    # --------------------------------------------------------

    return {
        "quiz_id": quiz.id,

        "title": quiz.title,

        "document_id": document.id,

        "document_name": document.filename,

        "difficulty": quiz.difficulty,

        "question_count": quiz.question_count,

        "questions": [
            {
                "id": question.id,

                "question": question.question,

                "topic": question.topic,

                "options": {
                    "A": question.option_a,
                    "B": question.option_b,
                    "C": question.option_c,
                    "D": question.option_d
                }
            }

            for question in saved_questions
        ]
    }


# ============================================================
# SUBMIT QUIZ
# ============================================================

@router.post("/submit")
def submit_quiz(
    request: SubmitQuizRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # --------------------------------------------------------
    # 1. Find quiz
    # --------------------------------------------------------

    quiz = (
        db.query(Quiz)
        .filter(
            Quiz.id == request.quiz_id,
            Quiz.user_id == current_user.id
        )
        .first()
    )

    if quiz is None:

        raise HTTPException(
            status_code=404,
            detail="Quiz not found."
        )


    # --------------------------------------------------------
    # 2. Get all questions belonging to this quiz
    # --------------------------------------------------------

    questions = (
        db.query(Question)
        .filter(
            Question.quiz_id == quiz.id
        )
        .all()
    )


    if not questions:

        raise HTTPException(
            status_code=400,
            detail="This quiz does not contain any questions."
        )


    # --------------------------------------------------------
    # 3. Create question lookup
    # --------------------------------------------------------

    question_lookup = {
        question.id: question
        for question in questions
    }


    # --------------------------------------------------------
    # 4. Prevent duplicate question IDs
    # --------------------------------------------------------

    submitted_question_ids = [
        answer.question_id
        for answer in request.answers
    ]

    if len(submitted_question_ids) != len(
        set(submitted_question_ids)
    ):

        raise HTTPException(
            status_code=400,
            detail="Duplicate question IDs were submitted."
        )


    # --------------------------------------------------------
    # 5. Validate submitted answers
    # --------------------------------------------------------

    for answer in request.answers:

        if answer.question_id not in question_lookup:

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Question ID "
                    f"{answer.question_id} "
                    f"does not belong to this quiz."
                )
            )


        selected = (
            answer.selected_answer
            .strip()
            .upper()
        )

        if selected not in [
            "A",
            "B",
            "C",
            "D"
        ]:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Selected answer must be "
                    "A, B, C, or D."
                )
            )


    # --------------------------------------------------------
    # 6. Evaluate answers
    # --------------------------------------------------------

    correct_count = 0

    results = []


    try:

        for answer in request.answers:

            question = question_lookup[
                answer.question_id
            ]


            selected = (
                answer.selected_answer
                .strip()
                .upper()
            )


            is_correct = (
                selected ==
                question.correct_answer
            )


            if is_correct:

                correct_count += 1


            # ------------------------------------------------
            # Save attempt
            # ------------------------------------------------

            attempt = QuizAttempt(
                user_id=current_user.id,

                quiz_id=quiz.id,

                question_id=question.id,

                selected_answer=selected,

                is_correct=(
                    1 if is_correct else 0
                ),

                time_taken=answer.time_taken
            )

            db.add(attempt)


            # ------------------------------------------------
            # Store result
            # ------------------------------------------------

            results.append(
                {
                    "question_id": question.id,

                    "topic": question.topic,

                    "selected_answer": selected,

                    "correct_answer": (
                        question.correct_answer
                    ),

                    "is_correct": is_correct,

                    "explanation": (
                        question.explanation
                    )
                }
            )


        # ----------------------------------------------------
        # Commit attempts
        # ----------------------------------------------------

        db.commit()


    except Exception as error:

        db.rollback()

        print(
            "Quiz submission error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "Failed to save quiz results. "
                "Please try again."
            )
        )


    # --------------------------------------------------------
    # 7. Calculate score
    # --------------------------------------------------------

    total = len(results)


    percentage = (
        (correct_count / total) * 100
        if total > 0
        else 0
    )


    # --------------------------------------------------------
    # 8. Return quiz result
    # --------------------------------------------------------

    return {
        "quiz_id": quiz.id,

        "total_questions": total,

        "correct_answers": correct_count,

        "incorrect_answers": (
            total - correct_count
        ),

        "score": correct_count,

        "percentage": round(
            percentage,
            2
        ),

        "results": results
    }