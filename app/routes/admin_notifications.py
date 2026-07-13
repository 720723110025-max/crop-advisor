from flask import Blueprint, render_template, request, redirect
from flask_login import login_required
from app.utils.database import db_instance
from datetime import datetime

admin_notification_bp = Blueprint(
    "admin_notification",
    __name__,
    url_prefix="/admin/notifications"
)

@admin_notification_bp.route("/")
@login_required
def index():

    notifications = list(
        db_instance.get_collection("notifications")
        .find()
        .sort("created_at", -1)
    )

    return render_template(
        "admin_notifications.html",
        notifications=notifications
    )


@admin_notification_bp.route("/send", methods=["POST"])
@login_required
def send():

    db_instance.get_collection("notifications").insert_one({

        "title": request.form["title"],

        "message": request.form["message"],

        "district": request.form["district"],

        "created_at": datetime.utcnow()

    })

    return redirect("/admin/notifications/")