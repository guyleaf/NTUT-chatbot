from flask import Flask, render_template, request, abort
from flask.wrappers import Response

from models import search_args_schema


app = Flask(__name__, static_folder="static")


@app.route("/search", methods=["GET"])
def get_search_page():
    user_id = request.args.get("user_id")
    if user_id is None:
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

    # TODO: Do something...

    title = "商品列表"
    products = [
        {
            "name": "3080",
            "brand": "ASUS",
            "price": 1000,
            "quantity": 5,
            "image_url": "https://cdn.vox-cdn.com/thumbor/Y8HSRGJGLdHmQlIkOFoA-jUtBzA=/0x0:2640x1749/1200x800/filters:focal(1109x664:1531x1086)/cdn.vox-cdn.com/uploads/chorus_image/image/69746324/twarren_rtx3080.0.jpg",
        },
        {
            "name": "3070",
            "brand": "ROG",
            "price": 800,
            "quantity": 0,
            "image_url": "https://cf.shopee.tw/file/e999d155a61197595757fa4945c589f9",
        },
        {
            "name": "3060",
            "brand": "ZOTAC",
            "price": 600,
            "quantity": 3,
            "image_url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZClI_bI7QUEtyZmPZs_VTx-DzQts0ScIs-g&usqp=CAU",
        },
    ]
    return render_template(
        "search/products.html", title=title, products=products
    )


@app.route("/<user_id>/myFavorite", methods=["GET", "POST"])
def get_my_favorite_page():
    title = "我的最愛"
    response = {
        "products": [
            {
                "name": "3080",
                "brand": "ASUS",
                "price": 1000,
                "quantity": 5,
                "image_url": "https://cdn.vox-cdn.com/thumbor/Y8HSRGJGLdHmQlIkOFoA-jUtBzA=/0x0:2640x1749/1200x800/filters:focal(1109x664:1531x1086)/cdn.vox-cdn.com/uploads/chorus_image/image/69746324/twarren_rtx3080.0.jpg",
            },
            {
                "name": "3070",
                "brand": "ROG",
                "price": 800,
                "quantity": 0,
                "image_url": "https://cf.shopee.tw/file/e999d155a61197595757fa4945c589f9",
            },
        ]
    }
    return render_template("myFavorite.html", **locals())


# buyer state:-1 處理中, 0 運送中 , 1已完成
# @app.route('/orderRecord/<userId>', methods=['GET', 'POST'])
@app.route("/orderRecord", methods=["GET", "POST"])
def orderRecord():
    title = "訂單紀錄"
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


# seller
# @app.route('/stockManagement/<userId>', methods=['GET', 'POST'])
@app.route("/stockManagement", methods=["GET", "POST"])
def stockManagement():
    title = "商品管理"
    response = {
        "products": [
            {
                "name": "3080",
                "brand": "ASUS",
                "price": 1000,
                "quantity": 5,
                "onShelf": 1,
                "image_url": "https://cdn.vox-cdn.com/thumbor/Y8HSRGJGLdHmQlIkOFoA-jUtBzA=/0x0:2640x1749/1200x800/filters:focal(1109x664:1531x1086)/cdn.vox-cdn.com/uploads/chorus_image/image/69746324/twarren_rtx3080.0.jpg",
            },
            {
                "name": "3070",
                "brand": "ROG",
                "price": 800,
                "quantity": 0,
                "onShelf": 0,
                "image_url": "https://cf.shopee.tw/file/e999d155a61197595757fa4945c589f9",
            },
        ]
    }
    return render_template("stockManagement.html", **locals())


# seller
# @app.route('/orderManagement/<userId>', methods=['GET', 'POST'])
@app.route("/orderManagement", methods=["GET", "POST"])
def orderManagement():
    title = "訂單管理"
    response = {
        "orders": [
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
    return render_template("orderManagement.html", **locals())


if __name__ == "__main__":
    app.run(debug=True)
