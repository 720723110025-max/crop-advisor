from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
import joblib
import pandas as pd

from app.models.soil_report import SoilReportModel

soil_bp = Blueprint(
    "soil",
    __name__,
    url_prefix="/soil"
)

model = SoilReportModel()

# Load AI model once
soil_model = joblib.load("models/soil_model.pkl")


@soil_bp.route("/")
@login_required
def index():

    reports = model.get_all()

    return render_template(
        "soil/index.html",
        reports=reports
    )


@soil_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    if request.method == "POST":

        image = request.files.get("soil_image")

        filename = ""

        if image and image.filename != "":

            filename = secure_filename(image.filename)

            upload_path = os.path.join(
                "app/static/uploads",
                filename
            )

            os.makedirs(
                "app/static/uploads",
                exist_ok=True
            )

            image.save(upload_path)

        # Read inputs
        nitrogen = float(request.form["nitrogen"])
        phosphorus = float(request.form["phosphorus"])
        potassium = float(request.form["potassium"])
        ph = float(request.form["ph"])

        # AI Prediction
        sample = pd.DataFrame([{
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "potassium": potassium,
            "ph": ph
        }])

        predicted_soil = soil_model.predict(sample)[0]

        # Recommendations
        if predicted_soil == "Fertile":
            crop = "Rice"
            fertilizer = "NPK 20-20-20"
            irrigation = "Every 5 days"
            health = "Excellent"

        elif predicted_soil == "Loamy":
            crop = "Maize"
            fertilizer = "DAP"
            irrigation = "Every 6 days"
            health = "Good"

        elif predicted_soil == "Clay":
            crop = "Sugarcane"
            fertilizer = "Urea"
            irrigation = "Every 7 days"
            health = "Moderate"

        elif predicted_soil == "Sandy":
            crop = "Groundnut"
            fertilizer = "Organic Compost"
            irrigation = "Every 3 days"
            health = "Poor"

        else:
            crop = "Millets"
            fertilizer = "Organic Compost"
            irrigation = "Every 4 days"
            health = "Average"

        data = {
            "farmer": current_user.username,
            "soil_image": filename,
            "soil_type": predicted_soil,
            "ph": ph,
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "potassium": potassium,
            "crop_recommendation": crop,
            "fertilizer": fertilizer,
            "irrigation": irrigation,
            "soil_health": health
        }

        model.create(data)

        flash("Soil Report Saved Successfully", "success")

        return redirect(url_for("soil.index"))

    return render_template("soil/upload.html")