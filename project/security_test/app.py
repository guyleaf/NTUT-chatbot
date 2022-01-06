from flask import Flask
from flask_jwt_extended import JWTManager

from logging import getLogger

from lineLoginClient import LineLoginClient
from models import db, User


app = Flask(__name__)
app.config.from_object("config")
app.logger = getLogger(__name__)

db.init_app(app)

jwt = JWTManager(app)

oauth_client = LineLoginClient(app)


@app.before_first_request
def setup():
    print("setup")
    db.create_all()


# @jwt.user_identity_loader
# def user_identity_lookup(user):
#     return user.id


# @jwt.user_lookup_loader
# def user_lookup_callback(_, jwt_data):
#     identity = jwt_data["sub"]
#     return User.query.filter_by(id=identity).one_or_none()
