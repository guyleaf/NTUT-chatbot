from flask import Blueprint, render_template, redirect, url_for, request
from flask_jwt_extended import current_user

from app import firestoreDAO
from enums import OrderStatusCode
from helpers import make_api_response
from decorators import roles_accepted
from schemas import new_order_schema, update_order_schema
from responses import (
    bad_request_message_for_api,
    product_not_found_message_for_api,
)


orders_resource = Blueprint(
    "orders",
    __name__,
    template_folder="templates",
    url_prefix="/orders",
)


@orders_resource.route("/", methods=["GET"])
@roles_accepted(["customer", "seller"], remember_endpoint=True)
def order_list_page():
    orders = firestoreDAO.get_orders(
        current_user.user.id, current_user.is_seller()
    )

    return render_template(
        "orders/orderList.html",
        orders=orders,
        is_seller=current_user.is_seller(),
    )


@orders_resource.route("/<order_id>", methods=["PUT"])
@roles_accepted(["customer", "seller"])
def update_order(order_id):
    order = request.get_json(force=True)
    errors = update_order_schema.validate(order)
    if errors:
        return (
            make_api_response(False, bad_request_message_for_api, errors),
            400,
        )

    order = update_order_schema.load(order)
    if (
        current_user.is_customer()
        and order["status_id"] != OrderStatusCode.CANCELLED
        and order["status_id"] != OrderStatusCode.FINISHED
    ):
        return (
            make_api_response(False, bad_request_message_for_api),
            401,
        )

    del order["status_id"]
    order.update(
        {f"status.{key}": value for key, value in order["status"].items()}
    )
    del order["status"]
    firestoreDAO.update_order(order_id, order)

    return make_api_response(True, "Update order successfully.")


@orders_resource.route("/", methods=["POST"])
@roles_accepted(["customer"])
def add_order():
    new_order = request.form.to_dict()
    errors = new_order_schema.validate(new_order)
    if errors:
        return (
            make_api_response(False, bad_request_message_for_api, errors),
            400,
        )

    new_order = new_order_schema.load(new_order)
    product = firestoreDAO.get_product_by_id(new_order["product_id"])
    if product is None:
        return (
            make_api_response(False, product_not_found_message_for_api),
            404,
        )

    new_order.setdefault("price", product["price"])
    new_order.setdefault("user_id", current_user.user.id)
    firestoreDAO.add_order(new_order)

    return redirect(url_for("resources.orders.order_list_page"))
