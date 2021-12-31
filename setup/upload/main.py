import flask
from typing import Any, Optional
import json

from firestoreDao import firestore_dao
from settings import admins


def init():
    with open("./product.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    for product in products:
        status_name = product["status"]
        product["status"] = {
            "quantity": product["quantity"],
            "is_available": status_name != "已下架" and status_name != "已刪除",
            "is_deleted": status_name == "已刪除",
        }
        del product["quantity"]

    firestore_dao.upload_products(products)


def register():
    firestore_dao.clear_user()
    for user in admins:
        firestore_dao.add_user(user)


def main(request: flask.Request):
    request_args = request.args

    if request_args["action"] == "register":
        register()
    elif request_args["action"] == "init":
        init()
    else:
        return "400 Bad Request", 400

    return "200 OK"
