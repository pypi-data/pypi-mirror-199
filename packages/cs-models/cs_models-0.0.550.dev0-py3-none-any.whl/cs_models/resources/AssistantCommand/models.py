from datetime import datetime
import enum
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, Text

from ...database import Base


class AssistantCommandTypeEnum(enum.Enum):
    SEARCH = "SEARCH"
    EXTRACT = "EXTRACT"
    SUMMARIZE = "SUMMARIZE"
    QUESTION_AND_ANSWER = "QUESTION_AND_ANSWER"


class AssistantCommandStatusEnum(enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    SUCCESSFUL = "SUCCESSFUL"


class AssistantCommandModel(Base):
    __tablename__ = "assistant_commands"

    id = Column(Integer, primary_key=True)
    user_query_id = Column(
        Integer,
        ForeignKey("assistant_user_queries.id"),
        nullable=False,
    )
    step_number = Column(Integer, nullable=False)
    type = Column("type", Enum(AssistantCommandTypeEnum))
    status = Column("status", Enum(AssistantCommandStatusEnum))
    label = Column(Text, nullable=False)
    result = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )
