import json
from flask import Flask, url_for, session, request
from flask import render_template, redirect
from werkzeug.urls import url_quote, url_unquote
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key = "!secret"
app.config.from_object("config")

CONF_URL = "https://accounts.google.com/.well-known/openid-configuration"
oauth = OAuth(app)
oauth.register(
    name="google",
    server_metadata_url=CONF_URL,
    client_kwargs={"scope": "openid email profile"},
)


def redirect_to_login(endpoint: str, **kwargs):
    return redirect(url_for("login", page=endpoint, **kwargs))


@app.route("/")
def home():
    user = session.get("user")
    return render_template("home.html", user=user)


@app.route("/redirect")
def redirect_route():
    page = request.args.get("page", "home")
    args = request.args.to_dict()
    if "page" in args:
        del args["page"]
    return redirect(url_for(page, **args))


@app.route("/test")
def test():
    user = session.get("user")
    if user is None:
        return redirect_to_login(request.endpoint)
    return user


@app.route("/login")
def login():
    redirect_uri = url_for("auth", _external=True)
    state = url_quote(json.dumps(request.args))
    return oauth.google.authorize_redirect(redirect_uri, state=state)


@app.route("/auth")
def auth():
    token = oauth.google.authorize_access_token()
    user = oauth.google.parse_id_token(token)
    if user:
        session["user"] = user

    state = url_unquote(request.args.get("state"))
    args = {}
    if state is not None:
        args = json.loads(state)
    return redirect(url_for("redirect_route", **args))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")
