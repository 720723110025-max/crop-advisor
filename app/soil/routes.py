from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.soil_report import SoilReportModel

soil_bp = Blueprint(
    "soil",
    __name__,
    url_prefix="/soil"
)

model = SoilReportModel()

@soil_bp.route("/")
def index():
    reports = model.get_all()
    return render_template("soil/index.html", reports=reports)

@soil_bp.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        data = {
            "farmer": "demo_user",
            "soil_type": request.form["soil_type"],
            "ph": request.form["ph"],
            "nitrogen": request.form["nitrogen"],
            "phosphorus": request.form["phosphorus"],
            "potassium": request.form["potassium"]
        }

        model.create(data)

        flash("Soil Report Saved Successfully", "success")

        return redirect(url_for("soil.index"))

    return render_template("soil/upload.html")