from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.expert import ExpertModel
from app.models.appointment import AppointmentModel
from flask_login import login_required, current_user

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
@login_required
def add():
 if current_user.role != "admin":

    flash("Only Admin can add experts.", "danger")

    return redirect(url_for("expert.index"))
 
    if request.method == "POST":

        expert_model.create({

    "name": request.form["name"],

    "username": request.form["username"],

    "password": request.form["password"],

    "district": request.form["district"],

    "specialization": request.form["specialization"],

    "languages": request.form["languages"],

    "experience": request.form["experience"],

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
@expert_bp.route("/edit/<expert_id>", methods=["GET", "POST"])
@login_required
def edit(expert_id):

    if current_user.role != "admin":

        flash("Access Denied", "danger")

        return redirect(url_for("expert.index"))

    expert = expert_model.get(expert_id)

    if request.method == "POST":

        expert_model.update(expert_id, {

            "name": request.form["name"],

            "district": request.form["district"],

            "specialization": request.form["specialization"],

            "languages": request.form["languages"],

            "experience": request.form["experience"],

            "phone": request.form["phone"],

            "email": request.form["email"],

            "availability": request.form["availability"]

        })

        flash("Expert Updated Successfully", "success")

        return redirect(url_for("expert.index"))

    return render_template(
        "expert/edit.html",
        expert=expert
    )
@expert_bp.route("/delete/<expert_id>")
@login_required
def delete(expert_id):

    if current_user.role != "admin":

        flash("Access Denied", "danger")

        return redirect(url_for("expert.index"))

    expert_model.delete(expert_id)

    flash("Expert Deleted Successfully", "success")

    return redirect(url_for("expert.index"))