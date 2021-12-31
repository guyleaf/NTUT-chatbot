from marshmallow import Schema, fields, validate


class Pagination(Schema):
    skip = fields.Integer(required=True, validate=validate.Range(min=0))
    take = fields.Integer(
        required=True, validate=validate.Range(min=1, max=50)
    )


class RegistrationSchema(Schema):
    line_id = fields.String(
        required=True, validate=validate.Length(min=1, max=120)
    )
    name = fields.String(required=True, validate=validate.Length(min=1))


class SearchArgsSchema(Pagination):
    user_id = fields.String(required=True)
    keyword = fields.String(required=True)


class MyFavoritesActionSchema(Schema):
    product_id = fields.String(required=True, validate=validate.Length(min=5))


registration_schema = RegistrationSchema()
search_args_schema = SearchArgsSchema()
my_favorites_action_schema = MyFavoritesActionSchema()
