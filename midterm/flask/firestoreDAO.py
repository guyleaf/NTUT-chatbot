from firebase_admin import firestore, initialize_app
from config import companyId
from publish import publish_messages
import threading

class FirestoreDAO:
    def __init__(self):
        initialize_app()
        self.__db = firestore.client()
    
    def getRole(self, userId):
        user = self.__db.document(f'users/{userId}')
        return user.role
    
    #myFavorite
    def getMyFavorites(self, userId):
        products =[]
        user_ref = self.collection('users').document(f'userId')
        favorites = user_ref.collection(f'users/{userId}/favorites')
        return favorites.get().to_dict()
        
    #search_result
    def getProducts(self, userId, keyword=None):
        products = []
        products_info = self.__db.collection('orders').where(keyword,'in','name').order_by('name').stream()
        for info in products_info:
            products.append(info)
        return products
    
    #orderRecord
    def getOrder(self, userId):
        orders = []
        orders_info = self.__db.collection('orders').where('userId','==',userId).order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
        for info in orders_info:
            orders.append(info._data)
        return orders
    
