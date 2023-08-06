from cs_models.resources.AssistantSession.schemas import AssistantSessionResourceSchema
from cs_models.resources.AssistantUserQuery.schemas import (
    AssistantUserQueryResourceSchema,
)
from src.cs_models.database import operations

from src.cs_models.resources.AssistantSession.models import AssistantSessionModel
from src.cs_models.resources.AssistantUserQuery.models import AssistantUserQueryModel
from src.cs_models.resources.AssistantCommand.models import (
    AssistantCommandModel,
    AssistantCommandTypeEnum,
    AssistantCommandStatusEnum,
)
from src.cs_models.resources.AssistantCommandEdge.models import (
    AssistantCommandEdgeModel,
)
from pprint import pprint

with operations.session_scope() as db_session:
    assistant_session = AssistantSessionModel(user_id="1000", label="Session 1")
    db_session.add(assistant_session)
    db_session.commit()

    user_query = AssistantUserQueryModel(
        session_id=assistant_session.id,
        value="Get me something",
    )
    db_session.add(user_query)
    db_session.commit()

    cmd1 = AssistantCommandModel(
        **{
            "user_query_id": user_query.id,
            "step_number": 1,
            "type": AssistantCommandTypeEnum.SEARCH,
            "label": "Search something",
            "status": AssistantCommandStatusEnum.NOT_STARTED,
            "result": None,
        },
    )
    cmd2 = AssistantCommandModel(
        **{
            "user_query_id": user_query.id,
            "step_number": 2,
            "type": AssistantCommandTypeEnum.EXTRACT,
            "label": "Extract something",
            "status": AssistantCommandStatusEnum.NOT_STARTED,
            "result": None,
        },
    )
    cmd3 = AssistantCommandModel(
        **{
            "user_query_id": user_query.id,
            "step_number": 3,
            "type": AssistantCommandTypeEnum.SUMMARIZE,
            "label": "Summarize",
            "status": AssistantCommandStatusEnum.NOT_STARTED,
            "result": None,
        },
    )

    AssistantCommandEdgeModel(cmd1, cmd2)
    AssistantCommandEdgeModel(cmd2, cmd3)
    db_session.add_all([cmd1, cmd2, cmd3])
    db_session.commit()

    pprint(AssistantSessionResourceSchema().dump(assistant_session))
