from datetime import datetime, timedelta, timezone
import os
from flask import Flask
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    set_access_cookies,
    get_jwt,
    get_jwt_identity,
)
from flask_jwt_extended.exceptions import NoAuthorizationError
from jwt.exceptions import InvalidSignatureError

from lineLoginClient import LineLoginClient
from settings import FlaskSettings, service_account_key_path
from models import db

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key_path

app = Flask(__name__, static_folder="static")
app.config.from_object(FlaskSettings)

db.init_app(app)

jwt = JWTManager(app)

oauth_client = LineLoginClient(app)


# Create a user to test with
@app.before_first_request
def initialize_db():
    db.create_all()


@app.errorhandler(InvalidSignatureError)
@app.errorhandler(NoAuthorizationError)
def jwt_exception_handler(exception):
    app.logger.exception(exception)
    return "Unauthorized", 401


@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original respone
        return response
