from flask import Blueprint, render_template, request, flash, redirect, url_for
from app.models.farmer import FarmerModel

# Create Blueprint FIRST
farmer_bp = Blueprint(
    "farmer",
    __name__,
    url_prefix="/farmer"
)

# Create Model
farmer_model = FarmerModel()


from app.utils.database import db_instance

@farmer_bp.route("/dashboard")
def dashboard():

    dashboard = {

        "lands": db_instance.get_collection("lands").count_documents({}),

        "crop_predictions": db_instance.get_collection(
            "crop_predictions"
        ).count_documents({}),

        "disease_reports": db_instance.get_collection(
            "disease_reports"
        ).count_documents({}),

        "workshops": db_instance.get_collection(
            "workshops"
        ).count_documents({})

    }

    recent_notifications = list(
        db_instance.get_collection("notifications")
        .find()
        .sort("created_at", -1)
        .limit(5)
    )

    return render_template(
        "farmer/dashboard.html",
        dashboard=dashboard,
        notifications=recent_notifications
    )
@farmer_bp.route("/profile", methods=["GET", "POST"])
def profile():

    user_id = "demo_user"

    farmer = farmer_model.get(user_id)

    if request.method == "POST":

        data = {

            "user_id": user_id,

            "name": request.form["name"],

            "phone": request.form["phone"],

            "district": request.form["district"],

            "village": request.form["village"],

            "land_size": request.form["land_size"]

        }

        if farmer:

            farmer_model.update(user_id, data)

        else:

            farmer_model.create(data)

        flash("Profile Saved Successfully", "success")

        return redirect(url_for("farmer.profile"))

    return render_template(
        "farmer/profile.html",
        farmer=farmer
    )

@farmer_bp.route("/lands")
def lands():
    return render_template("lands/index.html")


@farmer_bp.route("/market")
def market():
    return render_template("market/index.html")


@farmer_bp.route("/notifications")
def notifications():
    return render_template("notifications/index.html")


@farmer_bp.route("/feedback")
def feedback():
    return render_template("feedback/index.html")