from flask import Blueprint, render_template, request, flash
import os

soil_bp = Blueprint(
    "soil",
    __name__,
    url_prefix="/soil"
)


@soil_bp.route("/")
def index():
    return render_template("soil/index.html")


@soil_bp.route("/analyze", methods=["POST"])
def analyze():

    image = request.files.get("soil_image")

    if not image:

        flash(
            "Please upload a soil image.",
            "danger"
        )

        return render_template("soil/index.html")

    upload_folder = "app/static/uploads"

    os.makedirs(upload_folder, exist_ok=True)

    filepath = os.path.join(
        upload_folder,
        image.filename
    )

    image.save(filepath)

    # Temporary AI Result
    result = {

        "soil_type": "Loamy Soil",

        "ph": "6.8",

        "nitrogen": "Medium",

        "phosphorus": "High",

        "potassium": "Medium",

        "recommended_crop": "Paddy",

        "fertilizer": "NPK 20:20:20"

    }

    return render_template(

        "soil/result.html",

        result=result,

        image=image.filename

    )