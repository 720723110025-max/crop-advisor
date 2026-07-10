from flask import Blueprint, render_template, request, redirect, url_for, flash

appointment_bp = Blueprint(
    "appointment",
    __name__,
    url_prefix="/appointment"
)

appointments = []


@appointment_bp.route("/")
def index():

    return render_template(
        "appointment/index.html",
        appointments=appointments
    )


@appointment_bp.route("/book/<expert_id>", methods=["GET", "POST"])
def book(expert_id):

    if request.method == "POST":

        appointment = {

            "expert_id": expert_id,

            "farmer": request.form.get("farmer"),

            "date": request.form.get("date"),

            "time": request.form.get("time"),

            "reason": request.form.get("reason")

        }

        appointments.append(appointment)

        flash(
            "Appointment Booked Successfully",
            "success"
        )

        return redirect(url_for("appointment.index"))

    return render_template(
        "appointment/book.html",
        expert_id=expert_id
    )