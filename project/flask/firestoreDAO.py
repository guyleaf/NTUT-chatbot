import random
from typing import Any
from firebase_admin import firestore, initialize_app

from settings import company_id


class FirestoreDAO:
    _db: firestore.firestore.Client

    def __init__(self):
        initialize_app()
        self._db = firestore.client()

    def _get_products_stream_by_keyword(
        self, keyword: str, skip: int, take: int, include_all: bool
    ):
        products_collection = self._db.collection_group("product_items").where(
            "company_id", "==", company_id
        )

        if not include_all:
            products_collection = products_collection.where(
                "status.is_available", "==", True
            ).where("status.is_deleted", "==", False)

        if len(keyword) != 0:
            query = products_collection.where("name", ">=", keyword).where(
                "name", "<=", keyword + "\uf8ff"
            )
        else:
            query = products_collection

        return (
            query.stream(),
            query.offset(skip).limit(take).order_by("name").stream(),
        )

    def _get_product_document_by_id(
        self, product_id: str
    ) -> firestore.firestore.DocumentSnapshot:
        products = (
            self._db.collection_group("product_items")
            .where("company_id", "==", company_id)
            .where("id", "==", product_id)
            .get()
        )
        return products[0] if len(products) != 0 else None

    def _get_products_stream_by_ids(self, product_ids: "list[str]"):
        return (
            self._db.collection_group("product_items")
            .where("company_id", "==", company_id)
            .where("id", "in", product_ids)
            .stream()
        )

    def initialize_data_for_user(self, user_id: str):
        user_document = self._db.collection(
            f"companies/{company_id}/users"
        ).document(user_id)

        user_document.create({"user_id": user_id, "favorite_product_ids": []})

    # search / products
    def get_products_by_keyword(
        self,
        skip: int,
        take: int,
        keyword: str = None,
        include_all: bool = False,
    ):
        total, results = self._get_products_stream_by_keyword(
            keyword, skip, take, include_all
        )
        return sum(1 for _ in total), [
            product.to_dict() for product in results
        ]

    def get_product_by_id(self, product_id: str) -> "dict[str, Any]":
        result = self._get_product_document_by_id(product_id)
        return result.to_dict() if result else None

    def get_products_by_ids(
        self, product_ids: "list[str]"
    ) -> "list[dict[str, Any]]":
        results = self._get_products_stream_by_ids(product_ids)
        return [product.to_dict() for product in results]

    def get_favorite_product_ids(self, user_id: str) -> "list[str]":
        return (
            self._db.document(f"companies/{company_id}/users/{user_id}")
            .get(["favorite_product_ids"])
            .to_dict()
            .get("favorite_product_ids", [])
        )

    # myFavorites
    def get_favorite_products(self, user_id: str) -> "list[dict[str, Any]]":
        favorite_product_ids = self.get_favorite_product_ids(user_id)
        return (
            self.get_products_by_ids(favorite_product_ids)
            if len(favorite_product_ids) != 0
            else []
        )

    def is_product_existed(self, product_id: str) -> bool:
        product = self._get_product_document_by_id(product_id)
        return product is not None

    def add_favorite(self, user_id: str, product_id: str):
        user_document = self._db.document(
            f"companies/{company_id}/users/{user_id}"
        )
        user_document.update(
            {
                "favorite_product_ids": firestore.firestore.ArrayUnion(
                    [product_id]
                )
            }
        )

    def delete_favorite(self, user_id: str, product_id: str):
        user_document = self._db.document(
            f"companies/{company_id}/users/{user_id}"
        )
        user_document.update(
            {
                "favorite_product_ids": firestore.firestore.ArrayRemove(
                    [product_id]
                )
            }
        )

    # orderRecord, orderManagement
    def get_orders(self, user_id):
        orders = []
        if self.is_admin(user_id):
            orders_collection = self._db.collection("orders").stream()
            orders = orders_collection.to_dict()
        else:
            orders_collection = (
                self._db.collection("orders")
                .where("user_id", "==", user_id)
                .order_by("timestamp", direction=firestore.Query.DESCENDING)
                .stream()
            )
            for info in orders_collection:
                orders.append(info._data)
        return orders

    def is_order_existed(self, order_id: str) -> bool:  # Ron wrote
        order_collection = (
            self._db.collection_group("orders")
            .where("id", "==", order_id)
            .get()
        )
        return len(order_collection) == 1

    #
    def add_order(self, user_id: str, order_info: dict):  # Ron wrote
        order_info["user_id"] = user_id
        order_info["timestamp"] = firestore.SERVER_TIMESTAMP
        self._db.collection("orders").add(order_info)

    # orderManagement
    def update_order(self, order_info):  # Ron wrote
        order_id = order_info["order_id"]
        order_doc = self._db.document(f"orders/{order_id}")
        order_doc.set(order_info)

    def add_product(self, product: "dict[str, Any]") -> int:
        transaction = self._db.transaction()
        # count shards
        products_collection = self._db.collection(
            f"companies/{company_id}/products"
        )
        total_shards = sum(1 for _ in products_collection.stream())

        shard_index = random.randint(0, total_shards - 1)
        shard_ref = self._db.document(
            f"companies/{company_id}/products/{shard_index}"
        )

        product_ref = self._db.collection(
            f"companies/{company_id}/products/{shard_index}/product_items"
        ).document()
        product.setdefault("id", product_ref.id)
        product.setdefault("company_id", company_id)
        product["status"].setdefault("is_deleted", False)

        @firestore.firestore.transactional
        def add_product(
            transaction: firestore.firestore.Transaction,
            shard_ref: firestore.firestore.DocumentReference,
            product_ref: firestore.firestore.DocumentReference,
            product: "dict[str, Any]",
        ):
            transaction.create(product_ref, product)
            transaction.update(
                shard_ref, {"count": firestore.firestore.Increment(1)}
            )

        add_product(transaction, shard_ref, product_ref, product)
        return product["id"]

    def delete_product(self, product_id):
        product = self._get_product_document_by_id(product_id)
        if product:
            product.reference.set({"status.is_deleted": True})

    def update_product(self, product_id: str, product: "dict[str, Any]"):
        transaction = self._db.transaction()
        product_ref = self._get_product_document_by_id(product_id).reference

        @firestore.firestore.transactional
        def update_product(
            transaction: firestore.firestore.Transaction,
            product_ref: firestore.firestore.DocumentReference,
            modified_contents: "dict[str, Any]",
        ):
            transaction.update(product_ref, modified_contents)

        update_product(transaction, product_ref, product)
