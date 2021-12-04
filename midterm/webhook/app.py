from linebot import WebhookHandler, LineBotApi
from logging import getLogger

from settings import channel_secret, channel_access_token
from dialogflow.dialogflowClient import DialogflowClient
from dialogflow.dialogflowHandler import DialogflowHandler
from richmenu import RichMenu
from firestoreDao import FirestoreDao


logger = getLogger("webhook")

webhook_handler = WebhookHandler(channel_secret)
line_bot_api = LineBotApi(channel_access_token)
dialogflow_client = DialogflowClient()
dialogflow_handler = DialogflowHandler()
richmenu = RichMenu(line_bot_api, channel_access_token)
firestore_dao = FirestoreDao()
