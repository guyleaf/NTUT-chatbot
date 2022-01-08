from marshmallow import Schema, fields, validate, EXCLUDE, pre_load


class Pagination(Schema):
    skip = fields.Integer(required=True, validate=validate.Range(min=0))
    take = fields.Integer(
        required=True, validate=validate.Range(min=1, max=50)
    )


class SearchArgsSchema(Pagination):
    keyword = fields.String(required=True)


class MyFavoritesActionSchema(Schema):
    product_id = fields.String(required=True, validate=validate.Length(min=5))


class ProductStatusSchema(Schema):
    quantity = fields.Integer(required=True, validate=validate.Range(min=0))
    is_available = fields.Boolean(required=True)


class ProductSchema(Schema):
    name = fields.String(required=True, validate=validate.Length(min=1))
    brand = fields.String(required=True, validate=validate.Length(min=1))
    price = fields.Integer(required=True, validate=validate.Range(min=0))
    status = fields.Nested(ProductStatusSchema, required=True)
    image = fields.Raw()

    @pre_load
    def convert_data_to_status(self, data, **kwargs):
        data["status"] = {
            "quantity": data["quantity"],
            "is_available": data["is_available"],
        }
        return data

    class Meta:
        unknown = EXCLUDE


search_args_schema = SearchArgsSchema()
my_favorites_action_schema = MyFavoritesActionSchema()
product_schema = ProductSchema()
