from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from datetime import datetime

from sqlalchemy.orm import relationship

from ..AssistantCommand.models import AssistantCommandModel
from ...database import Base


class AssistantUserQueryModel(Base):
    __tablename__ = "assistant_user_queries"

    id = Column(Integer, primary_key=True)
    session_id = Column(
        Integer,
        ForeignKey("assistant_sessions.id"),
        nullable=False,
    )
    value = Column(
        String,
        nullable=False,
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=lambda: datetime.utcnow(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        # https://stackoverflow.com/questions/58776476/why-doesnt-freezegun-work-with-sqlalchemy-default-values
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
    )

    # These are ORM fields. Don't need to be added in the corresponding migration.
    # https://docs.sqlalchemy.org/en/14/orm/tutorial.html#building-a-relationship
    session = relationship(
        "AssistantSessionModel",
        back_populates="user_queries",
    )
    commands = relationship(
        "AssistantCommandModel",
        order_by=AssistantCommandModel.step_number,
        back_populates="user_query",
    )
