from flask import request, Blueprint, render_template
from flask_jwt_extended import jwt_required, current_user

from app import firestoreDAO
from decorators import roles_accepted
from helpers import make_api_response

from schemas import search_args_schema
from responses import bad_request_message_for_api


products_resource = Blueprint(
    "products",
    __name__,
    template_folder="templates",
    url_prefix="/products",
)


@products_resource.route("/search", methods=["GET"])
@jwt_required()
@roles_accepted(["customer", "seller"])
def search_page():
    title = "商品搜尋"
    return render_template("products/search.html", title=title)


@products_resource.route("/search", methods=["POST"])
@jwt_required()
@roles_accepted(["customer", "seller"])
def search_products():
    search_args = request.get_json(force=True)
    errors = search_args_schema.validate(search_args)

    if errors:
        return (
            make_api_response(False, bad_request_message_for_api, errors),
            400,
        )

    search_args = search_args_schema.load(search_args)

    favorite_product_ids = firestoreDAO.get_favorite_product_ids(
        current_user.id
    )
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
        "products/productList.html",
        title=title,
        product_infos=product_infos,
        total=total,
    )


@products_resource.route("/<product_id>", methods=["GET"])
@jwt_required()
@roles_accepted(["customer", "seller"])
def product_page(product_id):
    products = firestoreDAO.get_products_by_ids([product_id])

    if len(products) == 0:
        return
    return f"Product ID: {product_id}"


# seller
@products_resource.route("/", methods=["GET"])
def new_product_page(user_id):
    title = "商品管理"
    produtcts = firestoreDAO.get_products(user_id)
    return render_template("productManagement.html", **locals())
