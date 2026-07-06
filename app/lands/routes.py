from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.land import LandModel
from bson import ObjectId

lands_bp = Blueprint("lands", __name__, url_prefix="/lands")

land_model = LandModel()


@lands_bp.route("/")
def index():
    lands = land_model.get_all()
    return render_template("lands/index.html", lands=lands)


@lands_bp.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        land_model.create({

            "land_name": request.form["land_name"],

            "district": request.form["district"],

            "village": request.form["village"],

            "area": request.form["area"],

            "soil_type": request.form["soil_type"],

            "previous_crop": request.form["previous_crop"],

            "current_crop": request.form["current_crop"]

        })

        flash("Land Added Successfully", "success")

        return redirect(url_for("lands.index"))

    return render_template("lands/add_land.html")
@lands_bp.route("/edit/<land_id>", methods=["GET", "POST"])
def edit(land_id):

    land = land_model.get_by_id(land_id)

    if not land:
        flash("Land not found.", "danger")
        return redirect(url_for("lands.index"))

    if request.method == "POST":

        data = {
            "land_name": request.form["land_name"],
            "district": request.form["district"],
            "village": request.form["village"],
            "area": request.form["area"],
            "soil_type": request.form["soil_type"],
            "previous_crop": request.form["previous_crop"],
            "current_crop": request.form["current_crop"]
        }

        land_model.update(land_id, data)

        flash("Land Updated Successfully", "success")

        return redirect(url_for("lands.index"))

    return render_template("lands/edit_land.html", land=land)


@lands_bp.route("/delete/<land_id>")
def delete(land_id):

    land_model.delete(land_id)

    flash("Land Deleted Successfully", "success")

    return redirect(url_for("lands.index"))