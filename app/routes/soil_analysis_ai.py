from flask import Blueprint, render_template, request, jsonify

soil_ai_bp = Blueprint(
    "soil_ai",
    __name__,
    url_prefix="/soil-ai"
)

@soil_ai_bp.route("/")
def index():
    return render_template("soil_ai.html")


@soil_ai_bp.route("/analyze", methods=["POST"])
def analyze():

    soil_type = request.form.get("soil")

    if soil_type == "Black":
        crop = "Cotton"
        fertilizer = "NPK 20:20:20"

    elif soil_type == "Red":
        crop = "Groundnut"
        fertilizer = "DAP"

    elif soil_type == "Alluvial":
        crop = "Rice"
        fertilizer = "Urea"

    else:
        crop = "Maize"
        fertilizer = "Organic Compost"

    return jsonify({

        "crop": crop,

        "fertilizer": fertilizer

    })