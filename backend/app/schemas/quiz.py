from pydantic import BaseModel, Field


class GenerateQuizRequest(BaseModel):

    document_id: int = Field(
        ...,
        description="Selected PDF document ID"
    )

    question_count: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of questions"
    )

    difficulty: str = Field(
        default="medium",
        description="Quiz difficulty"
    )


class SubmitAnswer(BaseModel):

    question_id: int

    selected_answer: str = Field(
        ...,
        min_length=1,
        max_length=1
    )

    time_taken: int | None = None


class SubmitQuizRequest(BaseModel):

    quiz_id: int

    answers: list[SubmitAnswer]