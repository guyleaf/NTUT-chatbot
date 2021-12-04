import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from typing import Any
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
        codes_collection = self._db.collection(u"codes")
        documents = (
            codes_collection.where("type", "==", "product_status")
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

    def clear_all(self):
        batch_action = self._db.batch()
        codes_collection = self._db.collection(u"codes")
        products_collection = self._db.collection(u"products")

        for product in products_collection.stream():
            batch_action.delete(product.reference)

        for code in codes_collection.stream():
            batch_action.delete(code.reference)

        batch_action.commit()

    def add_user(self, user: dict[str, Any]):
        user_document = self._db.collection(u"users").document()

        user["id"] = user_document.id
        user_document.create(user)


firestore_dao = FirestoreDao()
