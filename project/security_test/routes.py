from flask import url_for, session, request, abort
from flask import render_template, redirect

from helpers import save_redirect_data, get_redirect_data
from app import app, db, jwt, oauth_client


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
        save_redirect_data(request.endpoint)
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
