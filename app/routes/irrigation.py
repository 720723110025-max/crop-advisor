from flask import Blueprint, render_template, request, jsonify

irrigation_bp = Blueprint(
    "irrigation",
    __name__,
    url_prefix="/irrigation"
)


@irrigation_bp.route("/")
def index():
    return render_template("irrigation.html")


@irrigation_bp.route("/api/irrigation-advice", methods=["POST"])
def irrigation_advice():

    crop = request.form.get("crop_type")

    moisture = float(request.form.get("soil_moisture"))

    temperature = float(request.form.get("temperature"))

    humidity = float(request.form.get("humidity"))

    rainfall = float(request.form.get("rainfall"))

    if moisture < 30:

        water = 1200
        method = "Drip Irrigation"
        duration = 3
        timing = "Morning"
        notes = "Soil is dry. Irrigate immediately."

    elif moisture < 60:

        water = 700
        method = "Sprinkler Irrigation"
        duration = 2
        timing = "Evening"
        notes = "Monitor moisture regularly."

    else:

        water = 300
        method = "No Irrigation Needed"
        duration = 0
        timing = "None"
        notes = "Enough moisture is available."

    if rainfall > 20:
        notes += " Rain is expected. Reduce irrigation."

    return jsonify({

        "success": True,

        "crop": crop,

        "water_requirement": water,

        "method": method,

        "duration": duration,

        "timing": timing,

        "notes": notes

    })