from flask import Blueprint

from decorators import jwt_required

reports_resource = Blueprint(
    "report", __name__, static_folder="templates", url_prefix="/report"
)


@reports_resource.route("/", methods=["GET"])
@jwt_required(remember_endpoint=True)
def report_page():
    return "Test"
