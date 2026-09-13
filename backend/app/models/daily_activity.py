from datetime import datetime, date

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)

from app.database import Base


class DailyActivity(Base):

    __tablename__ = "daily_activity"

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

    activity_date = Column(
        Date,
        nullable=False,
        index=True,
        default=date.today
    )

    study_time = Column(
        Integer,
        nullable=False,
        default=0
    )

    questions_attempted = Column(
        Integer,
        nullable=False,
        default=0
    )

    questions_correct = Column(
        Integer,
        nullable=False,
        default=0
    )

    quiz_score = Column(
        Float,
        nullable=False,
        default=0.0
    )

    quizzes_completed = Column(
        Integer,
        nullable=False,
        default=0
    )

    topics_studied = Column(
        String(1000),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "activity_date",
            name="unique_user_daily_activity"
        ),
    )