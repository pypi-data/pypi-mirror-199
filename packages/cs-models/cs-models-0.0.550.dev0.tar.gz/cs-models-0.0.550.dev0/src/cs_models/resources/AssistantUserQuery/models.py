from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Enum,
)
from datetime import datetime
from ...database import Base


class AssistantUserQueryModel(Base):
    __tablename__ = "assistant_user_queries"

    id = Column(Integer, primary_key=True)
    session_id = Column(
        Integer,
        ForeignKey("assistant_sessions.id"),
        nullable=False,
    )
    query = Column(
        String,
        nullable=False,
    )
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
