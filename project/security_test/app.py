from flask import Flask, url_for, session, request, abort
from flask import render_template, redirect
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


def save_redirect_data():
    session["redirect_data"] = {"page": request.endpoint}


def get_redirect_data() -> dict:
    return session.pop("redirect_data", {})


@app.before_first_request
def setup():
    print("setup")
    db.create_all()


@app.route("/")
def home():
    user = session.get("user")
    return render_template("home.html", user=user)


@app.route("/redirect")
def redirect_route():
    page = request.args.get("page", "home")
    return redirect(url_for(page))


@app.route("/test")
def test():
    user = session.get("user")
    if user is None:
        save_redirect_data()
        return redirect(url_for("login"))

    return user


@app.route("/login")
def login():
    redirect_uri = url_for("auth", _external=True)
    return oauth_client.authorize_redirect(redirect_uri)


@app.route("/auth")
def auth():
    code = request.args.get("code")
    state = request.args.get("state")
    if code is None or state is None:
        abort(400)

    user = oauth_client.authorize_access_token()
    if user is None:
        abort(400)

    session["user"] = user
    return redirect(url_for("redirect_route", **get_redirect_data()))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")
