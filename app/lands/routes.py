from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models.land import LandModel

lands_bp = Blueprint("lands", __name__, url_prefix="/lands")

land_model = LandModel()


@lands_bp.route("/")
@login_required
def index():

    lands = land_model.get_by_user(current_user.id)

    return render_template(
        "lands/index.html",
        lands=lands
    )


@lands_bp.route("/add", methods=["GET", "POST"])
@login_required
def add():

    if request.method == "POST":

        data = {

            "user_id": current_user.id,

            "land_name": request.form.get("land_name"),

            "district": request.form.get("district"),

            "block": request.form.get("block"),

            "village": request.form.get("village"),

            "area": request.form.get("area"),

            "soil_type": request.form.get("soil_type"),

            "previous_crop": request.form.get("previous_crop"),

            "current_crop": request.form.get("current_crop"),

            "gps_latitude": request.form.get("gps_latitude"),

            "gps_longitude": request.form.get("gps_longitude"),

            "soil_image": request.form.get("soil_image"),

            "yield_history": [],

            "estimated_profit": 0

        }

        land_model.create(data)

        flash(
            "Land Added Successfully",
            "success"
        )

        return redirect(url_for("lands.index"))

    return render_template("lands/add_land.html")


@lands_bp.route("/edit/<land_id>", methods=["GET", "POST"])
@login_required
def edit(land_id):

    land = land_model.get(land_id)

    if not land:

        flash(
            "Land not found.",
            "danger"
        )

        return redirect(url_for("lands.index"))

    if request.method == "POST":

        data = {

            "land_name": request.form.get("land_name"),

            "district": request.form.get("district"),

            "block": request.form.get("block"),

            "village": request.form.get("village"),

            "area": request.form.get("area"),

            "soil_type": request.form.get("soil_type"),

            "previous_crop": request.form.get("previous_crop"),

            "current_crop": request.form.get("current_crop"),

            "gps_latitude": request.form.get("gps_latitude"),

            "gps_longitude": request.form.get("gps_longitude"),

            "soil_image": request.form.get("soil_image")

        }

        land_model.update(land_id, data)

        flash(
            "Land Updated Successfully",
            "success"
        )

        return redirect(url_for("lands.index"))

    return render_template(
        "lands/edit_land.html",
        land=land
    )


@lands_bp.route("/delete/<land_id>")
@login_required
def delete(land_id):

    land_model.delete(land_id)

    flash(
        "Land Deleted Successfully",
        "success"
    )

    return redirect(url_for("lands.index"))