from flask import Flask

from linebot import LineBotApi
from linebot.models import TextSendMessage
from richmenu import RichMenu


registered_message = "註冊成功\n歡迎，顧客 {}"
functional_explain_message_for_customer = TextSendMessage(
    text="我們提供\n"
    + "1. 查詢 GPU：\n"
    + "查詢 GPU 商品資料，提供加入我的最愛功能，追蹤庫存狀況、價格異動等推播通知\n"
    + "2. 我的最愛：\n"
    + "檢視已追蹤的 GPU 商品資料\n"
    + "3. 訂單紀錄：\n"
    + "查詢 GPU 購買紀錄\n"
    + "4. 市場統計：\n"
    + "查看 GPU 市場統計"
)


class LineBotClient:
    _CHANNEL_ACCESS_TOKEN: str
    _CHANNEL_SECRET_TOKEN: str
    _line_bot_api: LineBotApi
    _rich_memu: RichMenu

    def __init__(self, app: Flask):
        self._CHANNEL_ACCESS_TOKEN = app.config["LINE_CHANNEL_ACCESS_TOKEN"]
        self._CHANNEL_SECRET_TOKEN = app.config["LINE_CHANNEL_SECRET_TOKEN"]
        self._line_bot_api = LineBotApi(self._CHANNEL_ACCESS_TOKEN)
        self._rich_memu = RichMenu(
            self._line_bot_api, self._CHANNEL_ACCESS_TOKEN
        )

    def push_registered_success_message(self, line_id: str, name: str):
        self._line_bot_api.push_message(
            line_id,
            TextSendMessage(registered_message.format(name)),
        )
        self._line_bot_api.push_message(
            line_id, functional_explain_message_for_customer
        )
        self._rich_memu.create(line_id)
