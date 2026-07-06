from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.workshop import WorkshopModel

workshop_bp = Blueprint(
    "workshops",
    __name__,
    url_prefix="/workshops"
)

model = WorkshopModel()

@workshop_bp.route("/")
def index():

    workshops = model.get_all()

    return render_template(
        "workshops/index.html",
        workshops=workshops
    )


@workshop_bp.route("/add", methods=["GET","POST"])
def add():

    if request.method == "POST":

        model.create({

            "title": request.form["title"],

            "date": request.form["date"],

            "time": request.form["time"],

            "district": request.form["district"],

            "mode": request.form["mode"],

            "capacity": request.form["capacity"],

            "description": request.form["description"]

        })

        flash("Workshop Added Successfully","success")

        return redirect(url_for("workshops.index"))

    return render_template("workshops/add.html")


@workshop_bp.route("/register/<workshop_id>")
def register(workshop_id):

    model.register({

        "workshop_id": workshop_id,

        "farmer": "demo_user"

    })

    flash("Workshop Registration Successful","success")

    return redirect(url_for("workshops.index"))