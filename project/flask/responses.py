# success response
add_favorite_product_successfully_message_for_api = (
    "Add product to my favorites successfully"
)
remove_favorite_product_successfully_message_for_api = (
    "Remove product from my favorites successfully"
)

# error response
bad_request_message_for_api = "Incorrect request format"
user_not_found_message_for_api = "Unknown user id"
product_not_found_message_for_api = "Unknown product id"
order_not_found_message_for_api = "Unknown order id"
user_not_found_message_for_view = "未知的使用者 ID"
user_missing_message_for_view = "缺少使用者 ID"
product_not_found_message_for_view = "未知的產品 ID"
service_exception_message = (
    "Service exception occurred. Please try again later."
)


def make_api_response(success: bool, message: str, data: dict = None) -> dict:
    return {"success": success, "message": message, "data": data}
