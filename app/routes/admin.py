from flask import Blueprint, render_template
from app.models.admin import AdminModel
from flask_login import login_required, current_user
from app.utils.database import db_instance
from app.utils.roles import admin_required

admin_bp = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)

model = AdminModel()

@admin_bp.route("/dashboard")
@login_required
@admin_required
def dashboard():

    stats = {

        "farmers":
        db_instance.get_collection("farmers").count_documents({}),

        "experts":
        db_instance.get_collection("experts").count_documents({}),

        "lands":
        db_instance.get_collection("lands").count_documents({}),

        "crop_predictions":
        db_instance.get_collection("crop_predictions").count_documents({}),

        "disease_reports":
        db_instance.get_collection("disease_reports").count_documents({}),

        "notifications":
        db_instance.get_collection("notifications").count_documents({})

    }

    latest_users = list(

        db_instance.get_collection("farmers")

        .find()

        .limit(5)

    )

    return render_template(

        "admin/dashboard.html",

        stats=stats,

        latest_users=latest_users

    )