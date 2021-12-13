import json
import os
from flask import Flask, render_template, request, abort, jsonify
from flask.wrappers import Response

from firestoreDAO import firestoreDAO
from models import (
    search_args_schema,
    my_favorites_action_schema,
    registration_schema,
)
from responses import (
    user_missing_message_for_view,
    user_not_found_message_for_view,
    user_not_found_message_for_api,
    product_not_found_message_for_api,
    service_exception_message,
)

app = Flask(__name__, static_folder="static")


@app.route("/register", methods=["POST"])
def register_user():
    registration_info = request.get_json(force=True)
    errors = registration_schema.validate(registration_info)

    if errors:
        return errors, 400

    registration_info = registration_schema.load(registration_info)

    if firestoreDAO.is_user_exists_by_line_id(registration_info["line_id"]):
        user = firestoreDAO.get_user(registration_info["line_id"])
    else:
        user = firestoreDAO.register_user(registration_info)

    if not user:
        return (
            {
                "success": False,
                "message": service_exception_message,
            },
            500,
        )

    return user


@app.route("/search", methods=["GET"])
def get_search_page():
    user_id = request.args.get("user_id")
    if not user_id:
        abort(Response(user_missing_message_for_view, 400))

    if not firestoreDAO.is_user_exists_by_id(user_id):
        abort(Response(user_not_found_message_for_view, 400))

    title = "商品搜尋"
    return render_template("search.html", title=title, user_id=user_id)


@app.route("/search", methods=["POST"])
def search_products():
    search_args = request.get_json(force=True)
    errors = search_args_schema.validate(search_args)

    if errors:
        return errors, 400

    search_args = search_args_schema.load(search_args)
    user_id = search_args["user_id"]

    if not firestoreDAO.is_user_exists_by_id(user_id):
        return {
            "success": False,
            "message": user_not_found_message_for_api,
        }, 404

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
        "search/products.html",
        title=title,
        product_infos=product_infos,
        total=total,
    )


@app.route("/<user_id>/myFavorites", methods=["GET"])
def get_my_favorite_page(user_id):
    if not firestoreDAO.is_user_exists_by_id(user_id):
        abort(Response(user_not_found_message_for_view, 400))

    title = "我的最愛"
    products = firestoreDAO.get_favorite_products(user_id)
    return render_template(
        "myFavorites.html", title=title, products=products, user_id=user_id
    )


@app.route("/<user_id>/myFavorites", methods=["POST"])
def add_favorite(user_id):
    body = request.get_json(force=True)
    errors = my_favorites_action_schema.validate(body)

    if errors:
        return errors, 400

    body = my_favorites_action_schema.load(body)

    product_id = body["product_id"]

    if not firestoreDAO.is_product_existed(product_id):
        return {
            "success": False,
            "message": product_not_found_message_for_api,
        }, 404
    if not firestoreDAO.is_user_exists_by_id(user_id):
        return {
            "success": False,
            "message": user_not_found_message_for_api,
        }, 404

    firestoreDAO.add_favorite(user_id, product_id)
    return jsonify("加入最愛成功")


@app.route("/<user_id>/myFavorites", methods=["DELETE"])
def delete_favorite(user_id):
    body = request.get_json(force=True)
    errors = my_favorites_action_schema.validate(body)

    if errors:
        return errors, 400

    body = my_favorites_action_schema.load(body)

    product_id = body["product_id"]

    if not firestoreDAO.is_product_existed(product_id):
        return {"success": False, "message": "Unknown product id"}, 404
    if not firestoreDAO.is_user_exists_by_id(user_id):
        return {"success": False, "message": "Unknown user id"}, 404

    firestoreDAO.delete_favorite(user_id, product_id)
    return jsonify("刪除最愛成功")


# buyer state:-1 處理中, 0 運送中 , 1已完成
@app.route("/<user_id>/orders", methods=["GET"])
def get_order_page(user_id):
    if not firestoreDAO.is_user_exists_by_id(user_id):
        abort(Response(user_not_found_message_for_view, 400))

    title = "我的最愛"
    orders = firestoreDAO.get_orders(user_id)
    return render_template(
        "orderRecord.html", title=title, orders=orders, user_id=user_id
    )


@app.route("/<user_id>/orders", methods=["PUT"])
def update_order(user_id):
    # Unable to get user_id (value is not in the form request) HAVE TO FIGURE OUT
    order_info = json.load(request.get_json(force=True))
    firestoreDAO.update_order(user_id, order_info)
    return jsonify("更新訂單成功")


@app.route("/<user_id>/orders", methods=["POST"])
def add_order(user_id):
    # Unable to get user_id (value is not in the form request) HAVE TO FIGURE OUT
    order_info = json.load(request.get_json(force=True))
    firestoreDAO.addOrder(user_id, order_info)
    return jsonify("新增訂單成功")


# seller
@app.route("/<user_id>/products", methods=["GET"])
def manage_products(user_id):
    title = "商品管理"
    produtcts = firestoreDAO.get_products(user_id)
    return render_template("productManagement.html", **locals())


# seller
@app.route("/<user_id>/orders", methods=["GET"])
def manage_orders(user_id):
    title = "訂單管理"
    orders = firestoreDAO.get_orders(user_id)
    return render_template("orderManagement.html", **locals())


@app.route("/<user_id>/products", methods=["POST"])
def add_product(user_id):
    product_info = json.load(request.get_json(force=True))
    firestoreDAO.add_product(product_info)
    return jsonify("新增商品成功")


@app.route("/<user_id>/products", methods=["PUT"])
def update_product(user_id):
    product_info = json.load(request.get_json(force=True))
    firestoreDAO.update_product(product_info)
    return jsonify("編輯商品成功")


port = int(os.environ.get("PORT", 8080))
if __name__ == "__main__":
    app.run(threaded=True, host="127.0.0.1", port=port)
