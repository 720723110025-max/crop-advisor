from flask import Blueprint, render_template

calendar_bp = Blueprint(
    "calendar",
    __name__,
    url_prefix="/calendar"
)

@calendar_bp.route("/")
def index():

    return render_template(
        "calendar/index.html"
    )