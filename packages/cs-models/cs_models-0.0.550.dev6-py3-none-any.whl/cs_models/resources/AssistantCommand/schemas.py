from marshmallow import (
    Schema,
    fields,
)

from ..AssistantCommand.models import AssistantCommandTypeEnum, AssistantCommandStatusEnum


class AssistantCommandResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_query_id = fields.Integer(required=True)
    step_number = fields.Integer(required=True)
    type = fields.Enum(AssistantCommandTypeEnum, required=True, by_value=True)
    label = fields.String(required=True)
    status = fields.Enum(AssistantCommandStatusEnum, required=True, by_value=True)
    result = fields.Dict(required=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
