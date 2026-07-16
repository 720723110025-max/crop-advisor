from flask import Blueprint, render_template
from collections import Counter

from app.utils.database import db_instance
from app.services.weather_service import get_weather

analytics_dashboard_bp = Blueprint(
    "analytics_dashboard",
    __name__,
    url_prefix="/analytics-dashboard"
)


@analytics_dashboard_bp.route("/")
def index():

    stats = {

        "farmers": db_instance.get_collection(
            "users"
        ).count_documents({}),

        "lands": db_instance.get_collection(
            "lands"
        ).count_documents({}),

        "crops": db_instance.get_collection(
            "crop_predictions"
        ).count_documents({}),

        "diseases": db_instance.get_collection(
            "disease_reports"
        ).count_documents({}),

        "appointments": db_instance.get_collection(
            "appointments"
        ).count_documents({}),

        "profits": db_instance.get_collection(
            "profit"
        ).count_documents({})

    }

    crop_history = list(
        db_instance.get_collection(
            "crop_predictions"
        ).find().sort(
            "created_at",
            -1
        ).limit(5)
    )

    disease_history = list(
        db_instance.get_collection(
            "disease_reports"
        ).find().sort(
            "created_at",
            -1
        ).limit(5)
    )

    weather = get_weather("Coimbatore")

    # Crop Statistics
    crop_names = [
        crop.get("recommended_crop", "Unknown")
        for crop in crop_history
    ]

    crop_chart = dict(
        Counter(crop_names)
    )

    # Disease Statistics
    disease_names = [
        disease.get("disease_name", "Unknown")
        for disease in disease_history
    ]

    disease_chart = dict(
        Counter(disease_names)
    )

    return render_template(

        "analytics_dashboard/index.html",

        stats=stats,

        crop_history=crop_history,

        disease_history=disease_history,

        crop_chart=crop_chart,

        disease_chart=disease_chart,

        weather=weather

    )