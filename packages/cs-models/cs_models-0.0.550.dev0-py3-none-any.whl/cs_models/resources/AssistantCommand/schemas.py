from marshmallow import (
    Schema,
    fields,
)


class AssistantCommandResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_query_id = fields.Integer(required=True)
    step_number = fields.Integer(required=True)
    type = fields.String(required=True)
    label = fields.String(required=True)
    status = fields.String(required=True)
    result = fields.Dict(required=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
