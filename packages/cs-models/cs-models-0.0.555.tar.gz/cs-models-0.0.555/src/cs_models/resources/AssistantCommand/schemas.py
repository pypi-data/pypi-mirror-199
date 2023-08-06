from marshmallow import (
    Schema,
    fields,
)

from ..AssistantCommand.models import (
    AssistantCommandModel,
    AssistantCommandTypeEnum,
    AssistantCommandStatusEnum,
)


class AssistantCommandResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_query_id = fields.Integer(required=True)
    step_number = fields.Integer(required=True)
    type = fields.Enum(AssistantCommandTypeEnum, required=True, by_value=True)
    label = fields.String(required=True)
    status = fields.Enum(AssistantCommandStatusEnum, required=True, by_value=True)
    higher_neighbour_ids = fields.Method(serialize="dump_higher_neighbours")
    lower_neighbour_ids = fields.Method(serialize="dump_lower_neighbours")
    result = fields.Dict(required=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    # https://marshmallow.readthedocs.io/en/stable/custom_fields.html#adding-context-to-method-and-function-fields
    def dump_higher_neighbours(self, obj: AssistantCommandModel):
        return [x.higher_id for x in obj.lower_edges]

    def dump_lower_neighbours(self, obj: AssistantCommandModel):
        return [x.lower_id for x in obj.higher_edges]
