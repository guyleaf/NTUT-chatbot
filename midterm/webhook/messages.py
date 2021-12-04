from helpers import get_text_send_message_object
from settings import product_type


_welcome_message = f"歡迎使用 {product_type} 購物小幫手"
welcome_message = get_text_send_message_object(_welcome_message)

register_handle_message = get_text_send_message_object("正在為您註冊...")
register_success_message = get_text_send_message_object("已完成註冊綁定")
register_failure_message = get_text_send_message_object("註冊失敗，請聯繫相關單位")

welcome_message_for_registered = "您好，{} {}\n"
functional_explain_message_for_customer = (
    "我們提供\n"
    + f"1. 查詢 {product_type}：\n"
    + f"查詢 {product_type} 商品資料，提供加入我的最愛功能，追蹤庫存狀況、價格異動等推播通知\n"
    + "2. 我的最愛：\n"
    + f"檢視已追蹤的 {product_type} 商品資料\n"
    + "3. 訂單紀錄：\n"
    + f"查詢 {product_type} 商品購買紀錄\n"
    + "4. 市場統計：\n"
    + f"查看 {product_type} 市場統計"
)
functional_explain_message_for_admin = (
    "我們提供\n"
    + f"1. 查詢 {product_type}：\n"
    + f"查詢 {product_type} 商品資料，提供加入我的最愛功能，追蹤庫存狀況、價格異動等推播通知\n"
    + "2. 我的最愛：\n"
    + f"檢視已追蹤的 {product_type} 商品資料\n"
    + "3. 管理訂單：\n"
    + f"管理 {product_type} 訂單\n"
    + "4. 管理商品：\n"
    + f"管理 {product_type} 商品資料\n"
    + "5. 統計報表：\n"
    + "查看業績統計報表"
)
