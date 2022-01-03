from flask import request, abort, Blueprint, Response, render_template

from app import firestoreDAO
from helpers import make_api_response

from schemas import search_args_schema
from responses import (
    bad_request_message_for_api,
    user_not_found_message_for_view,
    user_not_found_message_for_api,
    user_missing_message_for_view,
)


products_resource = Blueprint(
    "products", __name__, template_folder="templates"
)


@products_resource.route("/search", methods=["GET"])
def get_search_page():
    user_id = request.args.get("user_id")
    if not user_id:
        abort(Response(user_missing_message_for_view, 400))

    if not firestoreDAO.is_user_exists_by_id(user_id):
        abort(Response(user_not_found_message_for_view, 400))

    title = "商品搜尋"
    return render_template("search.html", title=title, user_id=user_id)


@products_resource.route("/search", methods=["POST"])
def search_products():
    search_args = request.get_json(force=True)
    errors = search_args_schema.validate(search_args)

    if errors:
        return (
            make_api_response(False, bad_request_message_for_api, errors),
            400,
        )

    search_args = search_args_schema.load(search_args)
    user_id = search_args["user_id"]

    if not firestoreDAO.is_user_exists_by_id(user_id):
        return (
            make_api_response(False, user_not_found_message_for_api),
            404,
        )

    favorite_product_ids = firestoreDAO.get_favorite_product_ids(user_id)
    total, products = firestoreDAO.get_products_by_keyword(
        search_args["skip"], search_args["take"], search_args["keyword"]
    )

    product_infos = []
    for product in products:
        product_info = None

        for favorite_product_id in favorite_product_ids:
            if product["id"] == favorite_product_id:
                product_info = {"is_favorite": True}
                break

        if product_info is None:
            product_info = {"is_favorite": False}

        product_info["product"] = product
        product_infos.append(product_info)

    title = "商品列表"
    return render_template(
        "shared/products.html",
        title=title,
        product_infos=product_infos,
        total=total,
    )


@products_resource.route("/products/<product_id>", methods=["GET"])
def get_product_page(product_id):
    products = firestoreDAO.get_products_by_ids([product_id])

    if len(products) == 0:
        return
    return f"Product ID: {product_id}"


@products_resource.route("/products/<product_id>", methods=["POST"])
def purchase_product(product_id):
    pass


# seller
@products_resource.route("/<user_id>/products", methods=["GET"])
def manage_products(user_id):
    title = "商品管理"
    produtcts = firestoreDAO.get_products(user_id)
    return render_template("productManagement.html", **locals())
