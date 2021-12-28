import os
from flask import Flask
from flask_security import (
    Security,
    SQLAlchemySessionUserDatastore,
)

from settings import FlaskSettings, service_account_key_path
from database import db_session, init_db
from models import User, Role

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_key_path

app = Flask(__name__, static_folder="static")
app.config.from_object(FlaskSettings)

user_datastore = SQLAlchemySessionUserDatastore(db_session, User, Role)
security = Security(app, user_datastore)


# Create a user to test with
@app.before_first_request
def initialize_db():
    init_db()
