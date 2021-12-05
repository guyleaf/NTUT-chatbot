import os
from typing import Any
from firebase_admin import firestore, initialize_app

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestoreServiceAccount.json"


class FirestoreDAO:
    _db: firestore.firestore.Client

    def __init__(self):
        initialize_app()
        self._db = firestore.client()

    def _get_products_stream_by_keyword(
        self, keyword: str, skip: int, take: int
    ):
        products_collection = self._db.collection_group("product_items")
        if keyword:
            query = products_collection.where("name", ">=", keyword).where(
                "name", "<=", keyword + "\uf8ff"
            )
        else:
            query = products_collection

        return (
            query.stream(),
            query.offset(skip).limit(take).order_by("name").stream(),
        )

    def _get_products_stream_by_ids(self, product_ids: list[str]):
        return (
            self._db.collection_group("product_items")
            .where("id", "in", product_ids)
            .stream()
        )

    def is_user_exists(self, user_id: str) -> bool:
        result = self._db.document(f"users/{user_id}").get()
        return result.exists

    def is_admin(self, user_id: str) -> bool:
        result = (
            self._db.document(f"users/{user_id}")
            .get(["is_admin"])
            .to_dict()
            .get("is_admin", False)
        )
        return result

    # search / products
    def get_products_by_keyword(
        self, skip: int, take: int, keyword: str = None
    ):
        total, results = self._get_products_stream_by_keyword(
            keyword, skip, take
        )
        return sum(1 for _ in total), [
            product.to_dict() for product in results
        ]

    def get_products_by_ids(
        self, product_ids: list[str]
    ) -> list[dict[str, Any]]:
        results = self._get_products_stream_by_ids(product_ids)
        return [product.to_dict() for product in results]

    def get_favorite_product_ids(self, user_id: str) -> list[str]:
        return (
            self._db.document(f"users/{user_id}")
            .get(["favorite_product_ids"])
            .to_dict()
            .get("favorite_product_ids", [])
        )

    # myFavorites
    def get_favorite_products(self, user_id: str) -> list[dict[str, Any]]:
        favorite_product_ids = self.get_favorite_product_ids(user_id)
        return self.get_products_by_ids(favorite_product_ids)

    def add_favorite(self, user_id, product_id):
        user_document = self._db.document(f"users/{user_id}")
        user_document.update(
            {
                "favorite_product_ids": firestore.firestore.ArrayUnion(
                    [product_id]
                )
            }
        )

    def delete_favorite(self, user_id, product_id):
        user_document = self._db.document(f"users/{user_id}")
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
            orders_col = self._db.collection("orders").stream()
            orders = orders_col.to_dict()
        else:
            orders_col = (
                self._db.collection("orders")
                .where("user_id", "==", user_id)
                .order_by("timestamp", direction=firestore.Query.DESCENDING)
                .stream()
            )
            for info in orders_col:
                orders.append(info._data)
        return orders

    #
    def add_order(self, user_id, order_info):
        order_info["user_id"] = user_id
        self._db.collection("orders").add(order_info)

    # orderManagement
    def update_order(self, order_info):
        order_id = order_info["order_id"]
        order_doc = self._db.collection("orders").document(f"{order_id}")
        order_doc.set(order_info)

    # stockManagement
    def add_product(self, product_info):
        self._db.collection("products").add(product_info)

    # stockManagement
    def update_product(self, product_info):
        product_id = product_info["product_id"]
        product_doc = self._db.collection("products").document(f"{product_id}")
        product_doc.set(product_info)


firestoreDAO = FirestoreDAO()
