from flask import Blueprint, render_template

location_bp = Blueprint(
    "location",
    __name__,
    url_prefix="/location"
)


@location_bp.route("/")
def index():

    return render_template(
        "location/index.html"
    )