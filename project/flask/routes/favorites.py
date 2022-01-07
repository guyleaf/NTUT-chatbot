from flask import Blueprint, request, render_template
from flask_jwt_extended import current_user
from flask_jwt_extended.view_decorators import jwt_required

from app import firestoreDAO
from decorators import roles_accepted
from helpers import make_api_response

from schemas import my_favorites_action_schema
from responses import (
    add_favorite_product_successfully_message_for_api,
    remove_favorite_product_successfully_message_for_api,
    bad_request_message_for_api,
    product_not_found_message_for_api,
)


favorites_resource = Blueprint(
    "favorites", __name__, template_folder="templates"
)


@favorites_resource.route("/myFavorites", methods=["GET"])
@jwt_required()
@roles_accepted(["customer", "seller"])
def get_my_favorite_page():
    products = firestoreDAO.get_favorite_products(current_user.user.id)

    product_infos = [
        {"is_favorite": True, "product": product} for product in products
    ]

    return render_template(
        "myFavorites.html",
        product_infos=product_infos,
        total=len(product_infos),
    )


@favorites_resource.route("/myFavorites", methods=["POST", "DELETE"])
@jwt_required()
@roles_accepted(["customer", "seller"])
def add_favorite():
    body = request.get_json(force=True)
    errors = my_favorites_action_schema.validate(body)
    if errors:
        return (
            make_api_response(False, bad_request_message_for_api, errors),
            400,
        )

    body = my_favorites_action_schema.load(body)

    product_id = body["product_id"]
    if not firestoreDAO.is_product_existed(product_id):
        return (
            make_api_response(False, product_not_found_message_for_api),
            404,
        )

    user_id = current_user.user.id
    if request.method == "POST":
        firestoreDAO.add_favorite(user_id, product_id)
        return make_api_response(
            True, add_favorite_product_successfully_message_for_api
        )
    else:
        firestoreDAO.delete_favorite(user_id, product_id)
        return make_api_response(
            True, remove_favorite_product_successfully_message_for_api
        )
