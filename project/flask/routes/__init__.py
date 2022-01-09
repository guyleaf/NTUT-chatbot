import json
from flask import request, redirect, url_for
from flask.blueprints import Blueprint

from .auth import auth_resource
from .products import products_resource
from .favorites import favorites_resource
from .orders import orders_resource
from .reports import reports_resource

resources = Blueprint("resources", __name__)

resources.register_blueprint(auth_resource)
resources.register_blueprint(products_resource)
resources.register_blueprint(favorites_resource)
resources.register_blueprint(orders_resource)
resources.register_blueprint(reports_resource)


@resources.route("/redirect")
def redirect_route():
    args = request.args.to_dict()
    page = args.get("page")
    return redirect(
        url_for(page, **json.loads(args["args"]))
        if page
        else "https://line.me/R/"
    )
