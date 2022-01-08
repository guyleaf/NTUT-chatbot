from flask import request, Blueprint, render_template, redirect, url_for
from flask_jwt_extended import current_user, get_jwt

from app import firestoreDAO
from decorators import roles_accepted
from helpers import make_api_response, now
from models import Product

from schemas import search_args_schema, product_schema
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
    product = firestoreDAO.get_product_by_id(product_id)

    if product is None:
        return redirect(url_for("resources.products.search_page"))

    template_name = None
    if current_user.is_seller():
        template_name = "products/updateProduct.html"
    else:
        template_name = "products/viewProduct.html"

    return_endpoint = request.args.get(
        "return_endpoint", "resources.products.search_page"
    )
    return render_template(
        template_name,
        product=product,
        return_endpoint=return_endpoint,
        csrf_token=get_jwt()["csrf"],
    )


@products_resource.route("/<product_id>", methods=["POST"])
@roles_accepted(["seller"])
def update_product(product_id):
    new_product = request.form.to_dict()
    errors = product_schema.validate(new_product)
    if errors:
        return (
            make_api_response(False, bad_request_message_for_api, errors),
            400,
        )

    new_product = product_schema.load(new_product)
    old_product = firestoreDAO.get_product_by_id(product_id)
    if old_product is None:
        return redirect(url_for("resources.products.search_page"))

    image = new_product.pop("image", None)
    if image:
        # Upload image
        pass

    new_status = new_product.pop("status")
    old_status = old_product.pop("status")
    # 取差集
    modified_contents = set(new_product.items()) - set(old_product.items())
    modified_status = set(new_status.items()) - set(old_status.items())
    if len(modified_contents) > 0 or len(modified_status) > 0:
        modified_contents = {key: value for key, value in modified_contents}
        modified_status = {
            f"status.{key}": value for key, value in modified_status
        }
        modified_contents.update(modified_status)
        modified_contents.setdefault("updated_time", now().timestamp())

        firestoreDAO.update_product(product_id, modified_contents)

    return redirect(
        url_for("resources.products.product_page", product_id=product_id)
    )


@products_resource.route("/<product_id>", methods=["DELETE"])
@roles_accepted(["seller"])
def delete_product(product_id):
    firestoreDAO.delete_product(product_id)
    return make_api_response(True, "Delete Successfully")


# seller
@products_resource.route("/", methods=["GET"])
@roles_accepted(["seller"], remember_endpoint=True)
def new_product_page():
    product = Product()
    # example
    # TODO: add upload image feature
    product.image_url = (
        "https://f.ecimg.tw/items/DRAD1K1900C81G9/000001_1640828679.jpg"
    )

    return render_template(
        "products/newProduct.html",
        product=product,
        csrf_token=get_jwt()["csrf"],
    )


@products_resource.route("/", methods=["POST"])
@roles_accepted(["seller"])
def add_product():
    new_product = request.form.to_dict()
    errors = product_schema.validate(new_product)
    if errors:
        return (
            make_api_response(False, bad_request_message_for_api, errors),
            400,
        )

    new_product = product_schema.load(new_product)
    # TODO: Add these features to updating and adding page
    new_product.setdefault("description", "")
    new_product.setdefault(
        "image_url",
        "https://f.ecimg.tw/items/DRAD1K1900C81G9/000001_1640828679.jpg",
    )
    new_product.setdefault("created_time", now().timestamp())
    new_product.setdefault("updated_time", now().timestamp())

    product_id = firestoreDAO.add_product(new_product)

    return redirect(
        url_for("resources.products.product_page", product_id=product_id)
    )
