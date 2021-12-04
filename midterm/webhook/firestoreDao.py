import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from settings import project_id


class FirestoreDao:
    _db: firestore.firestore.Client

    def __init__(self):
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {"project_id": project_id})
        self._db = firestore.client()

    def get_role_name(self, role_id: str) -> str:
        document = (
            self._db.collection("codes").where("id", "==", role_id).get()
        )[0].to_dict()

        return document["name"]
