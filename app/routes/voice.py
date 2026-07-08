from flask import Blueprint, render_template

voice_bp = Blueprint(
    "voice",
    __name__,
    url_prefix="/voice"
)

@voice_bp.route("/")
def index():
    return render_template("voice.html")