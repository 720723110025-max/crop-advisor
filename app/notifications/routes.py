from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.notification import NotificationModel

notification_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/notifications"
)

model = NotificationModel()


@notification_bp.route("/")
def index():

    notifications = model.get_all()

    return render_template(
        "notifications/index.html",
        notifications=notifications
    )


@notification_bp.route("/add", methods=["GET","POST"])
def add():

    if request.method == "POST":

        model.create({

            "title": request.form["title"],

            "message": request.form["message"],

            "district": request.form["district"]

        })

        flash("Notification Sent Successfully","success")

        return redirect(url_for("notifications.index"))

    return render_template("notifications/add.html")