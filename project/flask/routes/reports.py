from flask import Blueprint, redirect

from settings import customer_report, others_report
from decorators import jwt_required, roles_accepted

reports_resource = Blueprint(
    "reports", __name__, static_folder="templates", url_prefix="/reports"
)


@reports_resource.route("/customer", methods=["GET"])
@jwt_required(optional=True, remember_endpoint=True)
def customer_report_page():
    return redirect(customer_report)


@reports_resource.route("/others", methods=["GET"])
@roles_accepted(["seller", "admin"], remember_endpoint=True)
def others_report_page():
    return redirect(others_report)
