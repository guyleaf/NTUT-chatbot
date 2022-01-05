import flask
import json

from firestoreDao import firestore_dao
from settings import company_ids


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

    for company_id in company_ids:
        firestore_dao.upload_products(company_id, products)


def main(request: flask.Request):
    request_args = request.args

    if request_args["action"] == "init":
        init()
    else:
        return "400 Bad Request", 400

    return "200 OK"
