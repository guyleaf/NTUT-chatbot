from datetime import datetime, timedelta, timezone


def make_api_response(success: bool, message: str, data: dict = None) -> dict:
    return {"success": success, "message": message, "data": data}


def now() -> datetime:
    return datetime.now(timezone(timedelta(hours=+8)))
