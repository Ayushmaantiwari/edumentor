from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app.models.user import User
from app.models.quiz import Quiz, Question, QuizAttempt
from app.models.document import Document
from app.utils.auth import get_current_user


router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"]
)


# ============================================================
# ANALYTICS OVERVIEW
# ============================================================

@router.get("/overview")
def get_analytics_overview(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # --------------------------------------------------------
    # Total quizzes
    # --------------------------------------------------------

    total_quizzes = (
        db.query(func.count(Quiz.id))
        .filter(
            Quiz.user_id == current_user.id
        )
        .scalar()
        or 0
    )


    # --------------------------------------------------------
    # Total attempts
    # --------------------------------------------------------

    total_attempts = (
        db.query(func.count(QuizAttempt.id))
        .filter(
            QuizAttempt.user_id == current_user.id
        )
        .scalar()
        or 0
    )


    # --------------------------------------------------------
    # Correct answers
    # --------------------------------------------------------

    correct_answers = (
        db.query(func.count(QuizAttempt.id))
        .filter(
            QuizAttempt.user_id == current_user.id,
            QuizAttempt.is_correct == 1
        )
        .scalar()
        or 0
    )


    # --------------------------------------------------------
    # Incorrect answers
    # --------------------------------------------------------

    incorrect_answers = total_attempts - correct_answers


    # --------------------------------------------------------
    # Overall accuracy
    # --------------------------------------------------------

    accuracy = (
        (correct_answers / total_attempts) * 100
        if total_attempts > 0
        else 0
    )


    # --------------------------------------------------------
    # Average quiz percentage
    # --------------------------------------------------------

    quiz_percentages = []

    user_quizzes = (
        db.query(Quiz)
        .filter(
            Quiz.user_id == current_user.id
        )
        .order_by(
            Quiz.created_at.desc()
        )
        .all()
    )


    recent_quizzes = []


    for quiz in user_quizzes:

        attempts = (
            db.query(QuizAttempt)
            .filter(
                QuizAttempt.quiz_id == quiz.id,
                QuizAttempt.user_id == current_user.id
            )
            .all()
        )

        if attempts:

            correct = sum(
                1
                for attempt in attempts
                if attempt.is_correct == 1
            )

            percentage = (
                (correct / len(attempts)) * 100
                if attempts
                else 0
            )

            quiz_percentages.append(
                percentage
            )

            document = (
                db.query(Document)
                .filter(
                    Document.id == quiz.document_id
                )
                .first()
            )

            recent_quizzes.append(
                {
                    "quiz_id": quiz.id,
                    "title": quiz.title,
                    "document_name": (
                        document.filename
                        if document
                        else "Unknown document"
                    ),
                    "difficulty": quiz.difficulty,
                    "total_questions": len(attempts),
                    "correct_answers": correct,
                    "percentage": round(
                        percentage,
                        2
                    ),
                    "created_at": (
                        quiz.created_at.isoformat()
                        if quiz.created_at
                        else None
                    )
                }
            )


    average_score = (
        sum(quiz_percentages)
        / len(quiz_percentages)
        if quiz_percentages
        else 0
    )


    # --------------------------------------------------------
    # Topic-wise performance
    # --------------------------------------------------------

    topic_data = {}


    topic_rows = (
        db.query(
            Question.topic,
            QuizAttempt.is_correct
        )
        .join(
            QuizAttempt,
            QuizAttempt.question_id == Question.id
        )
        .filter(
            QuizAttempt.user_id == current_user.id
        )
        .all()
    )


    for topic, is_correct in topic_rows:

        topic_name = (
            topic.strip()
            if topic
            else "General"
        )

        if topic_name not in topic_data:

            topic_data[topic_name] = {
                "topic": topic_name,
                "attempted": 0,
                "correct": 0,
                "incorrect": 0
            }


        topic_data[topic_name]["attempted"] += 1


        if is_correct == 1:

            topic_data[topic_name]["correct"] += 1

        else:

            topic_data[topic_name]["incorrect"] += 1


    topic_performance = []


    for data in topic_data.values():

        attempted = data["attempted"]
        correct = data["correct"]

        topic_accuracy = (
            (correct / attempted) * 100
            if attempted > 0
            else 0
        )

        topic_performance.append(
            {
                "topic": data["topic"],
                "attempted": attempted,
                "correct": correct,
                "incorrect": data["incorrect"],
                "accuracy": round(
                    topic_accuracy,
                    2
                )
            }
        )


    topic_performance.sort(
        key=lambda item: item["accuracy"],
        reverse=True
    )


    # --------------------------------------------------------
    # Performance over recent quizzes
    # --------------------------------------------------------

    performance_history = []


    for quiz in reversed(recent_quizzes):

        performance_history.append(
            {
                "quiz_id": quiz["quiz_id"],
                "title": quiz["title"],
                "percentage": quiz["percentage"],
                "created_at": quiz["created_at"]
            }
        )


    # --------------------------------------------------------
    # Return analytics
    # --------------------------------------------------------

    return {
        "summary": {
            "total_quizzes": total_quizzes,
            "total_attempts": total_attempts,
            "correct_answers": correct_answers,
            "incorrect_answers": incorrect_answers,
            "accuracy": round(
                accuracy,
                2
            ),
            "average_score": round(
                average_score,
                2
            )
        },

        "topic_performance": topic_performance,

        "recent_quizzes": recent_quizzes[:10],

        "performance_history": performance_history[-10:]
    }

# ============================================================
# DASHBOARD
# ============================================================

@router.get("/dashboard")
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # --------------------------------------------------------
    # Documents
    # --------------------------------------------------------

    total_documents = (
        db.query(func.count(Document.id))
        .filter(
            Document.user_id == current_user.id
        )
        .scalar()
        or 0
    )


    # --------------------------------------------------------
    # Quiz count
    # --------------------------------------------------------

    total_quizzes = (
        db.query(func.count(Quiz.id))
        .filter(
            Quiz.user_id == current_user.id
        )
        .scalar()
        or 0
    )


    # --------------------------------------------------------
    # Attempts
    # --------------------------------------------------------

    total_attempts = (
        db.query(func.count(QuizAttempt.id))
        .filter(
            QuizAttempt.user_id == current_user.id
        )
        .scalar()
        or 0
    )


    # --------------------------------------------------------
    # Correct answers
    # --------------------------------------------------------

    correct_answers = (
        db.query(func.count(QuizAttempt.id))
        .filter(
            QuizAttempt.user_id == current_user.id,
            QuizAttempt.is_correct == 1
        )
        .scalar()
        or 0
    )


    # --------------------------------------------------------
    # Accuracy
    # --------------------------------------------------------

    accuracy = (
        (correct_answers / total_attempts) * 100
        if total_attempts > 0
        else 0
    )


    # --------------------------------------------------------
    # Recent documents
    # --------------------------------------------------------

    recent_documents = (
        db.query(Document)
        .filter(
            Document.user_id == current_user.id
        )
        .order_by(
            Document.uploaded_at.desc()
        )
        .limit(5)
        .all()
    )


    documents = []

    for document in recent_documents:

        documents.append(
            {
                "id": document.id,
                "filename": document.filename,
                "uploaded_at": (
                    document.uploaded_at.isoformat()
                    if document.uploaded_at
                    else None
                )
            }
        )


    # --------------------------------------------------------
    # Recent quizzes
    # --------------------------------------------------------

    recent_quizzes = (
        db.query(Quiz)
        .filter(
            Quiz.user_id == current_user.id
        )
        .order_by(
            Quiz.created_at.desc()
        )
        .limit(5)
        .all()
    )


    quizzes = []

    for quiz in recent_quizzes:

        attempts = (
            db.query(QuizAttempt)
            .filter(
                QuizAttempt.quiz_id == quiz.id,
                QuizAttempt.user_id == current_user.id
            )
            .all()
        )

        correct = sum(
            1
            for attempt in attempts
            if attempt.is_correct == 1
        )

        percentage = (
            (correct / len(attempts)) * 100
            if attempts
            else 0
        )

        quizzes.append(
            {
                "id": quiz.id,
                "title": quiz.title,
                "difficulty": quiz.difficulty,
                "total_questions": len(attempts),
                "correct_answers": correct,
                "percentage": round(
                    percentage,
                    2
                ),
                "created_at": (
                    quiz.created_at.isoformat()
                    if quiz.created_at
                    else None
                )
            }
        )


    # --------------------------------------------------------
    # Return dashboard
    # --------------------------------------------------------

    return {
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email
        },

        "stats": {
            "total_documents": total_documents,
            "total_quizzes": total_quizzes,
            "total_attempts": total_attempts,
            "correct_answers": correct_answers,
            "accuracy": round(
                accuracy,
                2
            )
        },

        "recent_documents": documents,

        "recent_quizzes": quizzes
    }