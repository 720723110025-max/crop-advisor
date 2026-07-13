from flask import Blueprint, render_template

analytics_dashboard_bp = Blueprint(
    "analytics_dashboard",
    __name__,
    url_prefix="/analytics-dashboard"
)


@analytics_dashboard_bp.route("/")
def index():

    stats = {
        "farmers": 120,
        "lands": 75,
        "crops": 45,
        "profit": 250000,
        "appointments": 38
    }

    return render_template(
        "analytics_dashboard/index.html",
        stats=stats
    )