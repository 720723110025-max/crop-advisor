from flask import Blueprint, render_template, request, redirect, url_for

irrigation_bp = Blueprint(
    "irrigation",
    __name__,
    url_prefix="/irrigation"
)

records = []


@irrigation_bp.route("/")
def index():

    return render_template(
        "irrigation/index.html",
        records=records
    )


@irrigation_bp.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        moisture = float(request.form.get("moisture"))

        crop = request.form.get("crop")

        if moisture < 30:
            recommendation = "Irrigation Required"

        elif moisture < 60:
            recommendation = "Monitor Soil Moisture"

        else:
            recommendation = "No Irrigation Needed"

        records.append({

            "crop": crop,

            "moisture": moisture,

            "recommendation": recommendation

        })

        return redirect(
            url_for("irrigation.index")
        )

    return render_template(
        "irrigation/add.html"
    )