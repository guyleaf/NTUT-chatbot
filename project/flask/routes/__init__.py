from flask import request, redirect, url_for
from flask.blueprints import Blueprint

from .auth import auth_resource
from .products import products_resource
from .favorites import favorites_resource

resources = Blueprint("resources", __name__)

resources.register_blueprint(auth_resource)
resources.register_blueprint(products_resource)
resources.register_blueprint(favorites_resource)


@resources.route("/redirect")
def redirect_route():
    page = request.args.get("page")
    return redirect(url_for(page) if page else "/")
