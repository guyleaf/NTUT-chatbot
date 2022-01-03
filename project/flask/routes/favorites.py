from flask import Blueprint, request, abort, Response, render_template

from app import firestoreDAO
from helpers import make_api_response

from schemas import my_favorites_action_schema
from responses import (
    add_favorite_product_successfully_message_for_api,
    remove_favorite_product_successfully_message_for_api,
    bad_request_message_for_api,
    user_not_found_message_for_view,
    user_not_found_message_for_api,
    product_not_found_message_for_api,
)


favorites_resource = Blueprint(
    "favorites", __name__, template_folder="templates"
)


@favorites_resource.route("/<user_id>/myFavorites", methods=["GET"])
def get_my_favorite_page(user_id):
    if not firestoreDAO.is_user_exists_by_id(user_id):
        abort(Response(user_not_found_message_for_view, 400))

    title = "我的最愛"
    products = firestoreDAO.get_favorite_products(user_id)

    product_infos = [
        {"is_favorite": True, "product": product} for product in products
    ]

    return render_template(
        "myFavorites.html",
        title=title,
        product_infos=product_infos,
        total=len(product_infos),
        user_id=user_id,
    )


@favorites_resource.route("/<user_id>/myFavorites", methods=["POST", "DELETE"])
def add_favorite(user_id):
    body = request.get_json(force=True)
    errors = my_favorites_action_schema.validate(body)

    if errors:
        return (
            make_api_response(False, bad_request_message_for_api, errors),
            400,
        )

    body = my_favorites_action_schema.load(body)

    product_id = body["product_id"]

    if not firestoreDAO.is_user_exists_by_id(user_id):
        return (
            make_api_response(False, user_not_found_message_for_api),
            404,
        )
    if not firestoreDAO.is_product_existed(product_id):
        return (
            make_api_response(False, product_not_found_message_for_api),
            404,
        )

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
