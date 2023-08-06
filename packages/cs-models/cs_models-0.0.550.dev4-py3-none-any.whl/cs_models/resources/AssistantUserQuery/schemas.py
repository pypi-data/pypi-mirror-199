from marshmallow import Schema, fields

from ..AssistantCommand.schemas import (
    AssistantCommandResourceSchema,
)


class AssistantUserQueryResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    session_id = fields.Integer(required=True)
    value = fields.String(required=True)
    commands = fields.Nested(AssistantCommandResourceSchema, many=True, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
