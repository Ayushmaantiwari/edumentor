from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text
)

from app.database import Base


# ============================================================
# QUIZ
# ============================================================

class Quiz(Base):

    __tablename__ = "quizzes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    document_id = Column(
        Integer,
        ForeignKey("documents.id"),
        nullable=False,
        index=True
    )

    title = Column(
        String(255),
        nullable=False
    )

    difficulty = Column(
        String(50),
        nullable=False,
        default="medium"
    )

    question_count = Column(
        Integer,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ============================================================
# QUESTION
# ============================================================

class Question(Base):

    __tablename__ = "questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id"),
        nullable=False,
        index=True
    )

    question = Column(
        Text,
        nullable=False
    )

    # Topic used for topic-wise analytics
    topic = Column(
        String(255),
        nullable=False,
        default="General"
    )

    option_a = Column(
        Text,
        nullable=False
    )

    option_b = Column(
        Text,
        nullable=False
    )

    option_c = Column(
        Text,
        nullable=False
    )

    option_d = Column(
        Text,
        nullable=False
    )

    correct_answer = Column(
        String(1),
        nullable=False
    )

    explanation = Column(
        Text,
        nullable=False
    )


# ============================================================
# QUIZ ATTEMPT
# ============================================================

class QuizAttempt(Base):

    __tablename__ = "quiz_attempts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id"),
        nullable=False,
        index=True
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False,
        index=True
    )

    selected_answer = Column(
        String(1),
        nullable=True
    )

    is_correct = Column(
        Integer,
        nullable=False,
        default=0
    )

    time_taken = Column(
        Integer,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )