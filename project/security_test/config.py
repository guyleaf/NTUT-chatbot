import os
import secrets
from datetime import timedelta

LINE_CLIENT_ID = os.getenv("CLIENT_ID")
LINE_CLIENT_SECRET = os.getenv("CLIENT_SECRET")

SECRET_KEY = secrets.token_urlsafe(16)
JWT_SECRET_KEY = secrets.token_urlsafe(16)
JWT_TOKEN_LOCATION = ["cookies", "headers"]
JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)

SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
SQLALCHEMY_TRACK_MODIFICATIONS = False
