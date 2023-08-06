from marshmallow import Schema, fields


class AssistantUserQueryResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    query = fields.String(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
