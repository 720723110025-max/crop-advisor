from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.utils.database import db_instance

analytics_bp = Blueprint(
    "analytics",
    __name__,
    url_prefix="/analytics"
)

@analytics_bp.route("/")
@login_required
def index():

    crop_count = db_instance.get_collection(
        "crop_predictions"
    ).count_documents({
        "user_id": str(current_user.id)
    })

    disease_count = db_instance.get_collection(
        "disease_reports"
    ).count_documents({
        "user_id": current_user.id
    })

    land_count = db_instance.get_collection(
        "lands"
    ).count_documents({})

    income = crop_count * 5000

    return render_template(
        "analytics.html",
        crop_count=crop_count,
        disease_count=disease_count,
        land_count=land_count,
        income=income
    )