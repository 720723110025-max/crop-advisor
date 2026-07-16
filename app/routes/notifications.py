from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.database import db_instance

notifications_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/notifications"
)

@notifications_bp.route("/")
@login_required
def index():

    notifications = list(
        db_instance.get_collection("notifications")
        .find()
        .sort("created_at", -1)
        .limit(20)
    )

    return render_template(
        "notifications.html",
        notifications=notifications
    )