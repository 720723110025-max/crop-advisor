from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.notification import NotificationModel
from flask_login import login_required, current_user

notification_bp = Blueprint(
    "notifications",
    __name__,
    url_prefix="/notifications"
)

model = NotificationModel()


@notification_bp.route("/")
@login_required
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

            "district": request.form["district"],

            "type": request.form["type"]

})

        flash("Notification Sent Successfully","success")

        return redirect(url_for("notifications.index"))

    return render_template("notifications/add.html")
@notification_bp.route("/delete/<id>")
@login_required
def delete(id):

    if current_user.role != "admin":

        flash("Access Denied","danger")

        return redirect(url_for("notifications.index"))

    model.delete(id)

    flash(

        "Notification Deleted",

        "success"

    )

    return redirect(url_for("notifications.index"))