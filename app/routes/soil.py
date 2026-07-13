from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os

from app.models.soil_report import SoilReportModel

soil_bp = Blueprint(
    "soil",
    __name__,
    url_prefix="/soil"
)

model = SoilReportModel()


@soil_bp.route("/")
@login_required
def index():

    reports = model.get_all()

    return render_template(
        "soil/index.html",
        reports=reports
    )


@soil_bp.route("/upload", methods=["GET","POST"])
@login_required
def upload():

    if request.method == "POST":

        image = request.files["soil_image"]

        filename = ""

        if image:

            filename = secure_filename(image.filename)

            image.save(
                os.path.join(
                    "app/static/uploads",
                    filename
                )
            )

        data = {

               "farmer": current_user.username,

                "soil_image": filename,

                "soil_type": request.form["soil_type"],

                "ph": request.form["ph"],

                "nitrogen": request.form["nitrogen"],

                "phosphorus": request.form["phosphorus"],

                "potassium": request.form["potassium"],

    # Temporary recommendations
                "crop_recommendation": "Rice",

                "fertilizer": "Urea",

                "irrigation": "Irrigate every 5 days",

                "soil_health": "Healthy"

    }

        model.create(data)

        flash("Soil Report Saved Successfully","success")

        return redirect(url_for("soil.index"))

    return render_template("soil/upload.html")