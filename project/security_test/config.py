import os
import secrets

LINE_CLIENT_ID = os.getenv("CLIENT_ID")
LINE_CLIENT_SECRET = os.getenv("CLIENT_SECRET")

SECRET_KEY = secrets.token_urlsafe(16)
JWT_SECRET_KEY = secrets.token_urlsafe(16)

SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
SQLALCHEMY_TRACK_MODIFICATIONS = False
