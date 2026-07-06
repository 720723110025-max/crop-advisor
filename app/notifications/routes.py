from flask import Blueprint, render_template

notification_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/notifications"
)

@notification_bp.route("/")
def index():
    return render_template("notifications/index.html")
