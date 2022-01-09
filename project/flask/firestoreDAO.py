import random
from typing import Any, Optional
from firebase_admin import firestore, initialize_app
from helpers import chunks, convert_timezone

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

    def get_product_by_id(self, product_id: str) -> Optional["dict[str, Any]"]:
        result = self._get_product_document_by_id(product_id)
        return result.to_dict() if result else None

    def get_products_by_ids(
        self, product_ids: "list[str]"
    ) -> "list[dict[str, Any]]":
        results = []
        for product_ids in chunks(product_ids, 10):
            result = self._get_products_stream_by_ids(product_ids)
            results.extend([product.to_dict() for product in result])

        return results

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
        print(favorite_product_ids)
        return self.get_products_by_ids(favorite_product_ids)

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

    def get_order_by_id(self, order_id: str):
        order_ref = self._db.document(
            f"companies/{company_id}/orders/{order_id}"
        ).get()
        return order_ref.to_dict()

    def get_orders(self, user_id: str, is_seller: bool):
        orders_collection = self._db.collection(
            f"companies/{company_id}/orders"
        )

        if not is_seller:
            orders_collection = orders_collection.where(
                "user_id", "==", user_id
            )

        orders_collection = orders_collection.order_by(
            "created_time", direction=firestore.firestore.Query.DESCENDING
        )

        orders = []
        for order in orders_collection.stream():
            order = order.to_dict()
            order["created_time"] = convert_timezone(order["created_time"])
            order["updated_time"] = convert_timezone(order["updated_time"])
            order.setdefault(
                "product_name",
                self.get_product_by_id(order["product_id"])["name"],
            )
            orders.append(order)

        return orders

    def add_order(self, order: "dict[str, Any]"):
        transaction = self._db.transaction()
        order_ref = self._db.collection(
            f"companies/{company_id}/orders"
        ).document()
        product_ref = self._get_product_document_by_id(
            order["product_id"]
        ).reference

        order.setdefault("id", order_ref.id)

        @firestore.firestore.transactional
        def add_order(
            transaction: firestore.firestore.Transaction,
            order_ref: firestore.firestore.DocumentReference,
            product_ref: firestore.firestore.DocumentReference,
            order: "dict[str, Any]",
        ):
            transaction.create(order_ref, order)
            transaction.update(
                product_ref,
                {
                    "status.quantity": firestore.firestore.Increment(
                        -order["quantity"]
                    )
                },
            )

        add_order(transaction, order_ref, product_ref, order)
        return order_ref.id

    def update_order(self, order_id: str, order: "dict[str, Any]"):
        order_ref = self._db.document(
            f"companies/{company_id}/orders/{order_id}"
        )
        order_ref.update(order)

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
        return product_ref.id

    def delete_product(self, product_id):
        product = self._get_product_document_by_id(product_id)
        if product:
            product.reference.update({"status.is_deleted": True})

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
