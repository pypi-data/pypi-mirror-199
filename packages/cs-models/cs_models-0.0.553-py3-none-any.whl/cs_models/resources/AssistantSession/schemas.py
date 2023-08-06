from marshmallow import Schema, fields

from ..AssistantUserQuery.schemas import AssistantUserQueryResourceSchema


class AssistantSessionResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    label = fields.String(required=True)
    user_queries = fields.Nested(AssistantUserQueryResourceSchema(exclude=("session_id",)), many=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
