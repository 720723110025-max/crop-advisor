from flask import Blueprint, render_template, request

crop_ai_bp = Blueprint(
    "crop_ai",
    __name__,
    url_prefix="/crop-ai"
)


@crop_ai_bp.route("/")
def index():
    return render_template("crop_ai/index.html")


@crop_ai_bp.route("/predict", methods=["POST"])
def predict():

    soil = request.form.get("soil")

    district = request.form.get("district")

    season = request.form.get("season")

    recommendation = {

        "crop": "Paddy",

        "seed": "Swarna",

        "yield": "5.5 Tons / Acre",

        "profit": "₹85,000"

    }

    return render_template(
        "crop_ai/result.html",
        recommendation=recommendation,
        soil=soil,
        district=district,
        season=season
    )