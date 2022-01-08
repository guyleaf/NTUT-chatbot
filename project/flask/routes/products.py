from flask import request, Blueprint, render_template, abort
from flask_jwt_extended import current_user

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
@roles_accepted(["customer", "seller"], remember_endpoint=True)
def search_page():
    return render_template(
        "products/search.html", is_customer=current_user.is_customer()
    )


@products_resource.route("/search", methods=["POST"])
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

    is_seller = current_user.is_seller()
    favorite_product_ids = firestoreDAO.get_favorite_product_ids(
        current_user.user.id
    )
    total, products = firestoreDAO.get_products_by_keyword(
        search_args["skip"],
        search_args["take"],
        search_args["keyword"],
        include_all=is_seller,
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

    return render_template(
        "products/productList.html",
        product_infos=product_infos,
        total=total,
        is_seller=is_seller,
    )


@products_resource.route("/<product_id>", methods=["GET"])
@roles_accepted(["customer", "seller"], remember_endpoint=True)
def product_page(product_id):
    product = firestoreDAO.get_products_by_id(product_id)

    if product is None:
        return abort(404)

    return render_template(
        "products/product.html",
        product=product,
        is_seller=current_user.is_seller(),
    )


# seller
@products_resource.route("/", methods=["GET"])
@roles_accepted(["seller"], remember_endpoint=True)
def new_product_page():
    title = "新增商品"
    return render_template("productManagement.html", **locals())
