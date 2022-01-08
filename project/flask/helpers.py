def make_api_response(success: bool, message: str, data: dict = None) -> dict:
    return {"success": success, "message": message, "data": data}
