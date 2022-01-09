from linebot.models import (
    TemplateSendMessage,
    CarouselTemplate,
    CarouselColumn,
    URITemplateAction,
)

from helpers import get_text_send_message_object
from settings import login_url


welcome_message = get_text_send_message_object("歡迎使用 GPU 購物小幫手")

register_message = TemplateSendMessage(
    alt_text="以下有新訊息...",
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                thumbnail_image_url="https://obs.line-scdn.net/0htYAKZc2HK3Z8MjzFDBdUIVhvIBRPUDV9XgYvEBlgACYNVxkgCy87dFFOECUWVwVERAc4eB9OEw8Ofh5LATUBaxI/f500x500",
                title="GPU-A 會員系統",
                text="你是新顧客，請註冊",
                actions=[
                    URITemplateAction(label="註冊", uri=login_url),
                ],
            )
        ]
    ),
)

functional_explain_message_for_customer = get_text_send_message_object(
    "我們提供\n"
    + "1. 查詢 GPU：\n"
    + "查詢 GPU 商品資料，提供加入我的最愛功能，追蹤庫存狀況、價格異動等推播通知\n"
    + "2. 我的最愛：\n"
    + "檢視已追蹤的 GPU 商品資料\n"
    + "3. 訂單紀錄：\n"
    + "查詢 GPU 購買紀錄\n"
    + "4. 市場統計：\n"
    + "查看 GPU 市場統計"
)

functional_explain_message_for_others = get_text_send_message_object(
    "我們提供\n"
    + "1. 查詢 GPU：\n"
    + "查詢 GPU 商品資料，提供加入我的最愛功能，追蹤庫存狀況、價格異動等推播通知\n"
    + "2. 我的最愛：\n"
    + "檢視已追蹤的 GPU 商品資料\n"
    + "3. 管理訂單：\n"
    + "管理 GPU 訂單\n"
    + "4. 管理商品：\n"
    + "管理 GPU 商品資料\n"
    + "5. 統計報表：\n"
    + "查看業績統計報表"
)
