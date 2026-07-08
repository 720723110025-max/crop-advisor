from flask import Blueprint, render_template, request, jsonify

soil_bp = Blueprint(
    "soil",
    __name__,
    url_prefix="/soil"
)

@soil_bp.route("/")
def index():
    return render_template("soil_analysis.html")


@soil_bp.route("/analyze", methods=["POST"])
def analyze():

    result = {

        "soil_type":"Red Soil",

        "ph":"6.8",

        "fertility":"High",

        "fertilizer":"NPK 19:19:19",

        "crops":"Rice, Maize, Groundnut"

    }

    return jsonify(result)