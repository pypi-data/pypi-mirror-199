from marshmallow import Schema, fields


class AssistantSessionResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
