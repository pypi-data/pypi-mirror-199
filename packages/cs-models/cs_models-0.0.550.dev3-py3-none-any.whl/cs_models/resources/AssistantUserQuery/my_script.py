from sqlalchemy.orm import joinedload

from cs_models.resources.AssistantSession.models import AssistantSessionModel
from cs_models.resources.AssistantSession.schemas import AssistantSessionResourceSchema
from cs_models.resources.AssistantUserQuery.models import AssistantUserQueryModel
from cs_models.resources.AssistantUserQuery.schemas import (
    AssistantUserQueryResourceSchema,
)
from cs_models.resources.AssistantCommand.models import AssistantCommandModel
from cs_models.resources.AssistantCommand.schemas import AssistantCommandResourceSchema

from cs_models.database import operations
from sqlalchemy import select, asc

from pprint import pprint


def main():
    with operations.session_scope() as db_session:
        # Get or create Assistant session
        assistant_session, _ = operations.get_or_create(
            session=db_session,
            model=AssistantSessionModel,
            schema=AssistantSessionResourceSchema,
            obj={"user_id": "auth0|1000"},
        )

        assistant_query, _ = operations.get_or_create(
            session=db_session,
            model=AssistantUserQueryModel,
            schema=AssistantUserQueryResourceSchema,
            obj={"session_id": assistant_session.id, "value": "get me 1"},
        )

        operations.get_or_create(
            session=db_session,
            model=AssistantCommandModel,
            schema=AssistantCommandResourceSchema,
            obj={
                "user_query_id": assistant_query.id,
                "step_number": 0,
                "type": "SEARCH",
                "label": "Search source 1",
                "status": "NOT_STARTED",
                "result": None,
            },
        )
        operations.get_or_create(
            session=db_session,
            model=AssistantCommandModel,
            schema=AssistantCommandResourceSchema,
            obj={
                "user_query_id": assistant_query.id,
                "step_number": 1,
                "type": "extract",
                "label": "Extract something",
                "status": "NOT_STARTED",
                "result": None,
            },
        )

        operations.get_or_create(
            session=db_session,
            model=AssistantUserQueryModel,
            schema=AssistantUserQueryResourceSchema,
            obj={"session_id": assistant_session.id, "value": "get me 2"},
        )

        pprint(AssistantSessionResourceSchema().dump(assistant_session))
        #


if __name__ == "__main__":
    main()
