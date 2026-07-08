from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.database import db_instance
from datetime import datetime

appointment_bp = Blueprint(
    "appointment",
    __name__,
    url_prefix="/appointment"
)


@appointment_bp.route("/")
@login_required
def index():

    experts = list(
        db_instance.get_collection("experts").find()
    )

    return render_template(
        "appointment.html",
        experts=experts
    )


@appointment_bp.route("/book", methods=["POST"])
@login_required
def book():

    appointment = {

        "farmer_id": str(current_user.id),

        "expert": request.form["expert"],

        "date": request.form["date"],

        "time": request.form["time"],

        "status": "Pending",

        "created_at": datetime.utcnow()

    }

    db_instance.get_collection(
        "appointments"
    ).insert_one(appointment)

    flash(
        "Appointment Booked Successfully",
        "success"
    )

    return redirect(
        url_for("appointment.history")
    )


@appointment_bp.route("/history")
@login_required
def history():

    appointments = list(

        db_instance.get_collection(
            "appointments"
        ).find({

            "farmer_id": str(current_user.id)

        })

    )

    return render_template(

        "appointment_history.html",

        appointments=appointments

    )