from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.crop import CropModel

crop_ai_bp = Blueprint(
    "crop_ai",
    __name__,
    url_prefix="/crop-ai"
)

model = CropModel()


@crop_ai_bp.route("/")
def index():

    history = model.get_all()

    return render_template(
        "crop_ai/index.html",
        history=history
    )


@crop_ai_bp.route("/predict", methods=["GET","POST"])
def predict():

    if request.method == "POST":

        district = request.form["district"]
        soil = request.form["soil"]

        if soil.lower() == "black":
            crop = "Cotton"

        elif soil.lower() == "red":
            crop = "Groundnut"

        else:
            crop = "Paddy"

        model.create({

            "district": district,

            "soil": soil,

            "recommended_crop": crop

        })

        flash("Crop Recommendation Generated","success")

        return redirect(url_for("crop_ai.index"))

    return render_template("crop_ai/predict.html")