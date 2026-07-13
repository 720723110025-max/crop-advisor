from flask import Blueprint, render_template, request, redirect, url_for, flash

workshop_bp = Blueprint(
    "workshop",
    __name__,
    url_prefix="/admin/workshops"
)

workshops = []


@workshop_bp.route("/")
def workshop_list():
    return render_template(
        "admin/workshops.html",
        workshops=workshops
    )


@workshop_bp.route("/add", methods=["GET", "POST"])
def add_workshop():

    if request.method == "POST":

        workshop = {
            "title": request.form["title"],
            "district": request.form["district"],
            "date": request.form["date"],
            "time": request.form["time"],
            "speaker": request.form["speaker"]
        }

        workshops.append(workshop)

        flash(
            "Workshop Added Successfully",
            "success"
        )

        return redirect(url_for("workshop.workshop_list"))

    return render_template("admin/add_workshop.html")