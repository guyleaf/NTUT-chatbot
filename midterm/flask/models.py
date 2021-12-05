from marshmallow import Schema, fields, validate


class Pagination(Schema):
    skip = fields.Integer(required=True, validate=validate.Range(min=0))
    take = fields.Integer(
        required=True, validate=validate.Range(min=1, max=50)
    )


class SearchArgsSchema(Pagination):
    user_id = fields.String(required=True)
    keyword = fields.String(required=True)


search_args_schema = SearchArgsSchema()
