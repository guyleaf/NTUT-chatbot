from marshmallow import Schema, fields, validate, EXCLUDE, pre_load

from enums import OrderStatusCode
from helpers import now


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


class OrderStatusSchema(Schema):
    is_confirmed = fields.Boolean(load_default=False)
    is_prepared = fields.Boolean(load_default=False)
    is_finished = fields.Boolean(load_default=False)
    is_cancelled = fields.Boolean(load_default=False)


class NewOrderSchema(Schema):
    product_id = fields.String(required=True, validate=validate.Length(min=5))
    quantity = fields.Integer(required=True, validate=validate.Range(min=1))
    status = fields.Nested(
        OrderStatusSchema,
        load_default={
            "is_confirmed": False,
            "is_prepared": False,
            "is_finished": False,
            "is_cancelled": False,
        },
    )
    created_time = fields.DateTime(load_default=now())
    updated_time = fields.DateTime(load_default=now())

    class Meta:
        unknown = EXCLUDE


class UpdateOrderSchema(Schema):
    status_id = fields.Integer(
        required=True,
        validate=validate.OneOf(list(map(lambda x: x.value, OrderStatusCode))),
    )
    status = fields.Nested(OrderStatusSchema, required=True)
    updated_time = fields.DateTime(load_default=now())

    @pre_load
    def convert_data_to_status(self, data, **kwargs):
        status = data["status_id"]
        data["status"] = {
            "is_confirmed": status == OrderStatusCode.CONFIRMED.value,
            "is_prepared": status == OrderStatusCode.PREPARED.value,
            "is_finished": status == OrderStatusCode.FINISHED.value,
            "is_cancelled": status == OrderStatusCode.CANCELLED.value,
        }
        return data


search_args_schema = SearchArgsSchema()
my_favorites_action_schema = MyFavoritesActionSchema()
product_schema = ProductSchema()
new_order_schema = NewOrderSchema()
update_order_schema = UpdateOrderSchema()
