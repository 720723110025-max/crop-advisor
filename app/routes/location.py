from flask import Blueprint, render_template
from flask_login import login_required

location_bp = Blueprint(
    "location",
    __name__,
    url_prefix="/location"
)

@location_bp.route("/")
@login_required
def index():

    return render_template(
        "location.html"
    )