import json
from flask import Flask, render_template, request, abort, jsonify
from flask.wrappers import Response

from firestoreDAO import firestoreDAO
from models import search_args_schema


app = Flask(__name__, static_folder="static")


@app.route("/search", methods=["GET"])
def get_search_page():
    user_id = request.args.get("user_id")
    if not user_id:
        abort(Response("缺少 user_id", 400))

    title = "商品搜尋"
    return render_template("search.html", title=title, user_id=user_id)


@app.route("/search", methods=["POST"])
def search_products():
    json_data = request.get_json(force=True)
    errors = search_args_schema.validate(json_data)

    if errors:
        return errors, 400

    search_args = search_args_schema.load(json_data)
    user_id = search_args["user_id"]

    if not firestoreDAO.is_user_exists(user_id):
        abort(Response("未知的使用者 ID", 400))

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


@app.route("/<user_id>/myFavorite", methods=["GET"])
def get_my_favorite_page(user_id):
    title = "我的最愛"
    products = firestoreDAO.get_favorite_products(user_id)
    return render_template("myFavorite.html", title=title, products=products)


@app.route("/<user_id>/myFavorite", methods=["POST"])
def add_favorite(user_id):
    # process product_info
    product_info = json.load(request.get_json(force=True))
    response = {
        "id": product_info["id"],
        "name": product_info["name"],
        "brand": product_info["brand"],
        "price": product_info["price"],
        "quantity": product_info["quantity"],
    }
    firestoreDAO.add_favorite(user_id, response)
    return jsonify("加入最愛成功")


@app.route("/<user_id>/myFavorite", methods=["DELETE"])
def delete_favorite(user_id):
    # process product_info
    product_info = json.load(request.get_json(force=True))
    firestoreDAO.delete_favorite(user_id, product_info["id"])
    return jsonify("刪除最愛成功")


# buyer state:-1 處理中, 0 運送中 , 1已完成
@app.route("/<user_id>/orders", methods=["GET"])
def get_order_page(user_id):
    title = "訂單紀錄"
    orders = firestoreDAO.get_orders(user_id)
    response = {
        "records": [
            {
                "name": "3080",
                "brand": "ASUS",
                "price": 1000,
                "quantity": 5,
                "date": "11/27",
                "state": 0,
                "image_url": "https://cdn.vox-cdn.com/thumbor/Y8HSRGJGLdHmQlIkOFoA-jUtBzA=/0x0:2640x1749/1200x800/filters:focal(1109x664:1531x1086)/cdn.vox-cdn.com/uploads/chorus_image/image/69746324/twarren_rtx3080.0.jpg",
            },
            {
                "name": "3070Ti",
                "brand": "MSI",
                "price": 800,
                "quantity": 1,
                "date": "11/29",
                "state": -1,
                "image_url": "https://cf.shopee.tw/file/e999d155a61197595757fa4945c589f9",
            },
            {
                "name": "3070",
                "brand": "ROG",
                "price": 800,
                "quantity": 1,
                "date": "12/01",
                "state": 1,
                "image_url": "https://cf.shopee.tw/file/e999d155a61197595757fa4945c589f9",
            },
        ]
    }
    return render_template("orderRecord.html", **locals())


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


if __name__ == "__main__":
    app.run(debug=True)
