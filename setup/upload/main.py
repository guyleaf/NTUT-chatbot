import flask
from typing import Any, Optional
import json

from firestoreDao import firestore_dao
from settings import admins


def init():
    with open("./code.json", "r", encoding="utf-8") as f:
        codes = json.load(f)

    firestore_dao.upload_code_data(codes)

    with open("./product.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    code_names = ["現貨", "缺貨中"]
    codes = firestore_dao.get_product_status_codes(code_names)

    def find_code(name: str) -> Optional[dict[str, Any]]:
        for code in codes:
            if code["name"] == name:
                return code
        return None

    for product in products:
        status_name = product["status"]
        product["status"] = {
            "quantity": product["quantity"],
            "status_id": find_code(status_name)["id"],
        }
        del product["quantity"]

    firestore_dao.upload_products(products)


def register():
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
