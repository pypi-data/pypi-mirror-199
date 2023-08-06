"""Models for storing Mindgram assistant sessions."""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from ...database import Base


class AssistantSessionModel(Base):
    """Model for storing Assistant Session."""

    __tablename__ = "assistant_sessions"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(128), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
