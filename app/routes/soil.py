from flask import Blueprint, render_template, request

soil_bp = Blueprint("soil", __name__)


@soil_bp.route("/soil", methods=["GET", "POST"])
def soil():

    result = None

    if request.method == "POST":

        ph = float(request.form["ph"])
        nitrogen = float(request.form["nitrogen"])
        phosphorus = float(request.form["phosphorus"])
        potassium = float(request.form["potassium"])

        # Soil Status
        if ph < 6:
            status = "Acidic Soil"
        elif ph > 8:
            status = "Alkaline Soil"
        else:
            status = "Healthy Soil"

        fertilizer = []

        if nitrogen < 50:
            fertilizer.append("Apply Urea")

        if phosphorus < 40:
            fertilizer.append("Apply DAP")

        if potassium < 40:
            fertilizer.append("Apply MOP")

        if len(fertilizer) == 0:
            fertilizer.append("No extra fertilizer required.")

        result = {
            "status": status,
            "fertilizer": fertilizer
        }

    return render_template(
        "soil.html",
        result=result
    )