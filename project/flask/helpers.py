from datetime import datetime, timedelta, timezone


def make_api_response(success: bool, message: str, data: dict = None) -> dict:
    return {"success": success, "message": message, "data": data}


def now() -> datetime:
    return datetime.now(timezone(timedelta(hours=+8)))


def convert_timezone(time: datetime) -> datetime:
    return time.astimezone(timezone(timedelta(hours=+8)))


def chunks(data: list, n: int):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(data), n):
        yield data[i:i+n]
