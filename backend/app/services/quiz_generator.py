import json
import re

from app.services.llm import generate_response


# ============================================================
# EXTRACT JSON FROM LLM RESPONSE
# ============================================================

def extract_json(text: str):

    text = text.strip()

    # Remove Markdown JSON code fences
    text = re.sub(
        r"```json\s*",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"```\s*$",
        "",
        text
    )

    # Find JSON object
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:

        raise ValueError(
            "LLM did not return valid JSON."
        )

    json_text = text[
        start:end + 1
    ]

    return json.loads(json_text)


# ============================================================
# GENERATE QUIZ
# ============================================================

def generate_quiz(
    context: str,
    question_count: int = 5,
    difficulty: str = "medium"
):

    system_prompt = """
You are EduMentor, an AI teaching assistant.

Your task is to create a multiple-choice quiz
using ONLY the provided study material.

IMPORTANT RULES:

1. Use ONLY the supplied study material.
2. Do NOT invent facts.
3. Every question must have exactly one
   correct answer.
4. Create exactly four options:
   A, B, C and D.
5. Options must be plausible.
6. Clearly identify the correct answer.
7. Provide an explanation for the correct answer.
8. Questions should test understanding,
   not only memorization.
9. Match the requested difficulty.
10. Assign ONE short topic to every question.
11. The topic must be directly related to
    the concept being tested.
12. Use concise topic names.
13. Examples of topic names:
    - Memory
    - Interrupts
    - Timers
    - GPIO
    - ARM Architecture
    - Registers
    - PWM
    - Embedded Systems
14. Do NOT create topics that are unrelated
    to the supplied material.
15. Return ONLY valid JSON.
16. Do NOT use Markdown.
17. Do NOT add text before or after JSON.

Required JSON format:

{
    "questions": [
        {
            "topic": "Timers",
            "question": "Question text",
            "option_a": "Option A",
            "option_b": "Option B",
            "option_c": "Option C",
            "option_d": "Option D",
            "correct_answer": "A",
            "explanation": "Explanation"
        }
    ]
}
"""

    user_prompt = f"""
Study Material
================================

{context}

================================

Generate exactly {question_count}
multiple-choice questions.

Difficulty:
{difficulty}

For every question:

- Identify the main topic.
- Create four options.
- Select exactly one correct answer.
- Provide an explanation.

Return ONLY the required JSON.
"""

    response = generate_response(
        prompt=user_prompt,
        system_prompt=system_prompt
    )

    quiz_data = extract_json(response)

    questions = quiz_data.get(
        "questions",
        []
    )

    # ========================================================
    # VALIDATE QUESTION COUNT
    # ========================================================

    if len(questions) != question_count:

        raise ValueError(
            f"Expected {question_count} questions "
            f"but received {len(questions)}."
        )

    # ========================================================
    # VALIDATE QUESTIONS
    # ========================================================

    required_fields = [
        "topic",
        "question",
        "option_a",
        "option_b",
        "option_c",
        "option_d",
        "correct_answer",
        "explanation"
    ]

    for question in questions:

        # Check fields
        for field in required_fields:

            if not question.get(field):

                raise ValueError(
                    f"Missing quiz field: {field}"
                )

        # Clean topic
        question["topic"] = (
            str(question["topic"])
            .strip()
        )

        if not question["topic"]:

            question["topic"] = "General"

        # Normalize answer
        question["correct_answer"] = (
            str(
                question["correct_answer"]
            )
            .strip()
            .upper()
        )

        # Validate answer
        if question["correct_answer"] not in [
            "A",
            "B",
            "C",
            "D"
        ]:

            raise ValueError(
                "Invalid correct answer."
            )

    return questions