from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.expert import ExpertModel
from app.models.appointment import AppointmentModel

# Create Blueprint FIRST
expert_bp = Blueprint(
    "expert",
    __name__,
    url_prefix="/expert"
)

# Models
expert_model = ExpertModel()
appointment_model = AppointmentModel()


@expert_bp.route("/")
def index():
    experts = expert_model.get_all()
    return render_template("expert/index.html", experts=experts)


@expert_bp.route("/add", methods=["GET", "POST"])
def add():

    if request.method == "POST":

        expert_model.create({
            "name": request.form["name"],
            "district": request.form["district"],
            "specialization": request.form["specialization"],
            "phone": request.form["phone"],
            "email": request.form["email"]
        })

        flash("Expert Added Successfully", "success")
        return redirect(url_for("expert.index"))

    return render_template("expert/add.html")


@expert_bp.route("/book/<expert_id>")
def book(expert_id):

    appointment_model.create({
        "expert_id": expert_id,
        "farmer": "demo_user",
        "status": "Pending"
    })

    flash("Appointment Booked Successfully", "success")

    return redirect(url_for("expert.index"))