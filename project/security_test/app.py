from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from logging import getLogger

from lineLoginClient import LineLoginClient


app = Flask(__name__)
app.config.from_object("config")
app.logger = getLogger(__name__)

db = SQLAlchemy(app)

jwt = JWTManager(app)

oauth_client = LineLoginClient(app)


@app.before_first_request
def setup():
    print("setup")
    db.create_all()
