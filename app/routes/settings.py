from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

settings_bp = Blueprint(
    "settings",
    __name__,
    url_prefix="/settings"
)


@settings_bp.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":

        current_user.full_name = request.form.get("full_name")

        current_user.phone = request.form.get("phone")

        current_user.language = request.form.get("language")

        flash(
            "Profile Updated Successfully",
            "success"
        )

        return redirect(url_for("settings.index"))

    return render_template(
        "settings/index.html"
    )