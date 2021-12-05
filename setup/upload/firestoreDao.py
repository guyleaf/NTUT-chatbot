import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from typing import Any
import datetime
import random

from settings import project_id


class Shard:
    """
    A shard is a distributed counter. Each shard can support being incremented
    once per second. Multiple shards are needed within a Counter to allow
    more frequent incrementing.
    """

    def __init__(self):
        self._count = 0

    def to_dict(self):
        return {"count": self._count}


class FirestoreDao:
    _db: firestore.firestore.Client
    _num_of_shards: int

    def __init__(self):
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {"project_id": project_id})
        self._db = firestore.client()
        self._num_of_shards = 10

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

    def _init_shards(self, collection):
        for num in range(self._num_of_shards):
            shard = Shard()
            collection.document(str(num)).set(shard.to_dict())

    def upload_products(self, products: list[dict[str, Any]]):
        products_collection = self._db.collection(u"products")
        self._init_shards(products_collection)

        batch_action = self._db.batch()

        for product in products:
            date_time = datetime.datetime.now()
            product["created_time"] = date_time
            product["updated_time"] = date_time

            # products_collection: [ <=== products_document
            #     {
            #         count: int,
            #         items_collection: [
            #             { <=== items_document
            #
            #             }
            #         ]
            #     }
            # ]

            # pick one document randomly
            # similar to get hashed value and select bucket
            document_id = random.randint(0, self._num_of_shards - 1)
            products_document = products_collection.document(str(document_id))

            items_collection = products_document.collection("product_items")
            items_document = items_collection.document(product["id"])
            batch_action.create(items_document, product)

            batch_action.update(
                products_document, {"count": firestore.firestore.Increment(1)}
            )

        batch_action.commit()

    def add_user(self, user: dict[str, Any]):
        user_document = self._db.collection(u"users").document()

        user["id"] = user_document.id
        user_document.create(user)


firestore_dao = FirestoreDao()
