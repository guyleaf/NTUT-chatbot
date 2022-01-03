import os

from flask import Flask
from flask_jwt_extended import JWTManager

from firestoreDAO import FirestoreDAO
from lineLoginClient import LineLoginClient
from settings import FlaskSettings, service_account_key_path
from models import db

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key_path


app = Flask(__name__, static_folder="static")
app.config.from_object(FlaskSettings)

db.init_app(app)

jwt = JWTManager(app)

oauth_client = LineLoginClient(app)

firestoreDAO = FirestoreDAO()
