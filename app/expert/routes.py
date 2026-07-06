from flask import Blueprint, render_template

expert_bp = Blueprint(
    "expert",
    __name__,
    url_prefix="/expert"
)

@expert_bp.route("/dashboard")
def dashboard():
    return render_template("expert/dashboard.html")

@expert_bp.route("/profile")
def profile():
    return render_template("expert/profile.html")

@expert_bp.route("/appointments")
def appointments():
    return render_template("expert/appointments.html")

@expert_bp.route("/chat")
def chat():
    return render_template("expert/chat.html")