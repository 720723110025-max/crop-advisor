from flask import Blueprint, render_template, request, jsonify

location_bp = Blueprint(
    "location",
    __name__,
    url_prefix="/location"
)

@location_bp.route("/")
def index():
    return render_template("location.html")


@location_bp.route("/recommend", methods=["POST"])
def recommend():

    latitude = float(request.form["latitude"])
    longitude = float(request.form["longitude"])

    if latitude > 10:
        crop = "Rice"
    else:
        crop = "Groundnut"

    return jsonify({
        "crop": crop,
        "latitude": latitude,
        "longitude": longitude
    })