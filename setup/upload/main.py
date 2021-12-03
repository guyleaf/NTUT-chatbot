import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from typing import Any, Optional
import json
import datetime

from settings import project_id


class FirestoreDao:
    _db: firestore.firestore.Client

    def __init__(self):
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {"project_id": project_id})
        self._db = firestore.client()

    def upload_code_data(self, data: list[dict[str, Any]]):
        batch_action = self._db.batch()
        codes_collection = self._db.collection(u"codes")

        for code in data:
            code_document = codes_collection.document(code["id"])
            batch_action.create(code_document, code)

        batch_action.commit()

    def get_product_status_codes(
        self, names: list[str]
    ) -> list[dict[str, Any]]:  # noqa: E501
        codes_document = self._db.collection(u"codes")
        documents = (
            codes_document.where("type", "==", "product_status")
            .where(u"name", u"in", names)
            .get()
        )

        return [document.to_dict() for document in documents]

    def upload_products(self, products: list[dict[str, Any]]):
        batch_action = self._db.batch()
        products_collection = self._db.collection(u"products")

        for product in products:
            date_time = datetime.datetime.now()
            product["created_time"] = date_time
            product["updated_time"] = date_time
            product_document = products_collection.document(product["id"])
            batch_action.create(product_document, product)

        batch_action.commit()


def main(_):
    with open("./code.json", "r", encoding="utf-8") as f:
        codes = json.load(f)

    firestore_dao = FirestoreDao()
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

    return "200 OK"
