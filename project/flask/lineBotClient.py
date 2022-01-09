from flask import Flask


class LineLoginClient:
    _CHANNEL_ACCESS_TOKEN: str
    _CHANNEL_SECRET_TOKEN: str

    def __init__(self, app: Flask):
        self._CHANNEL_ACCESS_TOKEN = app.config["LINE_CHANNEL_ACCESS_TOKEN"]
        self._CHANNEL_SECRET_TOKEN = app.config["LINE_CHANNEL_SECRET_TOKEN"]
