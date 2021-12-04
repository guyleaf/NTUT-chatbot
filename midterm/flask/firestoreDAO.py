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
    def getFavorites(self, userId):
        user_ref = self.collection('users').document(f'userId')
        favorites_col = user_ref.collection(f'users/{userId}/favorites')
        return favorites_col.get().to_dict()
        
    #search_result / stockManagement
    def getProducts(self, userId, keyword=None):
        products = []
        if keyword : #search
            products_col = self.__db.collection('orders').where(keyword,'in','name').order_by('name').stream()
            products = products_col.to_dict()
            #for info in products_col:
            #    products.append(info)
        elif self.getRole(userId) == 'admin':
            products_col = self.__db.collection('orders').stream()
            products = products_col.to_dict()
        return products
    
    #orderRecord, orderManagement
    def getOrder(self, userId):
        orders = []
        if self.getRole() == 'admin':
            orders_col = self.__db.collection('orders').stream()
            orders = orders_col.to_dict()
        elif self.getRole() == 'customer':
            orders_col = self.__db.collection('orders').where('userId','==',userId).order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
            for info in orders_col:
                orders.append(info._data)
        return orders
    
    #
    def setFavorites(self, userId, productInfo):
        user_ref = self.__db.collection('users').document(f'{userId}')
        favorites_col = user_ref.collection('favorites')
        favorites_col.set(productInfo)
    
    #
    def deleteFavorites(self, userId, productId):
        favorite_ref = self.__db.collection('users/{userId}/favorites')
        product_doc = favorite_ref.document('productId')
        product_doc.delete()
        
    #
    def addOrder(self, userId, orderInfo):
        orderInfo['userId'] = userId
        self.__db.collection('orders').add(orderInfo)
    #orderManagement
    def updateOrder(self, orderInfo):
        orderId = orderInfo['orderId']
        order_doc = self.__db.collection('orders').document(f'{orderId}')
        order_doc.set(orderInfo)
    
    #stockManagement
    def addProduct(self, productInfo):
        self.__db.collection('products').add(productInfo)
    #stockManagement
    def updateProduct(self, productInfo):
        productId = productInfo['productId']
        product_doc = self.__db.collection('products').document(f'{productId}')
        product_doc.set(productInfo)

