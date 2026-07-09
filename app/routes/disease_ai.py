from flask import Blueprint, render_template, request
import os

disease_ai_bp = Blueprint(
    "disease_ai",
    __name__,
    url_prefix="/disease-ai"
)


@disease_ai_bp.route("/")
def index():
    return render_template("disease_ai/index.html")


@disease_ai_bp.route("/predict", methods=["POST"])
def predict():

    image = request.files.get("crop_image")

    if not image:
        return render_template(
            "disease_ai/index.html",
            error="Please upload an image."
        )

    upload_folder = "app/static/uploads"

    os.makedirs(upload_folder, exist_ok=True)

    image.save(
        os.path.join(upload_folder, image.filename)
    )

    result = {

        "disease": "Leaf Blast",

        "confidence": "98%",

        "organic":

        "Neem Oil Spray every 7 days",

        "chemical":

        "Tricyclazole 75WP",

        "prevention":

        "Avoid excess nitrogen fertilizer"

    }

    return render_template(

        "disease_ai/result.html",

        image=image.filename,

        result=result

    )