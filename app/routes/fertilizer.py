from flask import Blueprint, render_template, request

fertilizer_bp = Blueprint(
    "fertilizer",
    __name__,
    url_prefix="/fertilizer"
)


@fertilizer_bp.route("/", methods=["GET", "POST"])
def index():

    recommendation = None

    if request.method == "POST":

        crop = request.form.get("crop")

        n = int(request.form.get("nitrogen"))
        p = int(request.form.get("phosphorus"))
        k = int(request.form.get("potassium"))

        if n < 50:
            recommendation = "Use Urea"

        elif p < 40:
            recommendation = "Use DAP"

        elif k < 40:
            recommendation = "Use MOP"

        else:
            recommendation = "NPK levels are balanced."

    return render_template(
        "fertilizer/index.html",
        recommendation=recommendation
    )