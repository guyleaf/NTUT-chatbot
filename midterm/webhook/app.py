from logging import getLogger
from linebot import WebhookHandler, LineBotApi

from settings import channel_secret, channel_access_token
from richmenu import RichMenu

logger = getLogger("webhook")
webhook_handler = WebhookHandler(channel_secret)
line_bot_api = LineBotApi(channel_access_token)
richmenu = RichMenu(line_bot_api, channel_access_token)
