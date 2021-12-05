import os
from firebase_admin import firestore, initialize_app

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "firestoreServiceAccount.json"


class FirestoreDAO:
    _db: firestore.firestore.Client

    def __init__(self):
        initialize_app()
        self._db = firestore.client()

    def get_role(self, user_id):
        user = self._db.document(f"users/{user_id}").get()
        return user.to_dict()

    # myFavorite
    def get_favorites(self, user_id):
        user_ref = self.collection("users").document("user_id")
        favorites_col = user_ref.collection(f"users/{user_id}/favorites")
        return favorites_col.get().to_dict()

    # search_result / stockManagement
    def get_products(
        self, user_id: str, skip: int, take: int, keyword: str = None
    ):
        products = []
        if keyword:  # search
            products_collection = (
                self._db.collection("orders")
                .where("name", ">=", keyword)
                .where("name", "<=", keyword + "\uf8ff")
                .offset(skip)
                .limit(take)
                .order_by("name")
                .get()
            )
            products = products_collection.to_dict()
        elif self.get_role(user_id)[""] == "admin":
            products_collection = (
                self._db.collection("orders")
                .offset(skip)
                .limit(take)
                .order_by("id")
                .get()
            )
            products = products_collection.to_dict()
        return products

    # orderRecord, orderManagement
    def get_orders(self, user_id):
        orders = []
        if self.getRole() == "admin":
            orders_col = self._db.collection("orders").stream()
            orders = orders_col.to_dict()
        elif self.getRole() == "customer":
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
    def add_favorite(self, user_id, product_info):
        user_ref = self._db.collection("users").document(f"{user_id}")
        favorites_col = user_ref.collection("favorites")
        favorites_col.set(product_info)

    #
    def delete_favorite(self, user_id, product_id):
        favorite_ref = self._db.collection(f"users/{user_id}/favorites")
        product_doc = favorite_ref.document("product_id")
        product_doc.delete()

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
