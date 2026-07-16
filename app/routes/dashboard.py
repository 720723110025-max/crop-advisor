"""
Dashboard routes for the main application dashboard.
"""

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.utils.database import db_instance
from app.services.weather_service import get_weather
from app.services.gemini_service import get_ai_tip

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
@login_required
def index():

    crop_predictions = list(
        db_instance.get_collection("crop_predictions")
        .find({"user_id": str(current_user.id)})
        .sort("created_at", -1)
        .limit(5)
    )

    disease_reports = list(
        db_instance.get_collection("disease_reports")
        .find({"user_id": current_user.id})
        .sort("created_at", -1)
        .limit(5)
    )

    stats = {
        "farmers": db_instance.get_collection("farmers").count_documents({}),
        "lands": db_instance.get_collection("lands").count_documents({}),
        "crops": db_instance.get_collection("crop_predictions").count_documents({}),
        "diseases": db_instance.get_collection("disease_reports").count_documents({})
    }

    try:
        weather = get_weather("Coimbatore")
        ai_tip = get_ai_tip(weather)
    except Exception:
        weather = {
        "temperature": 32,
        "condition": "Sunny",
        "humidity": 68,
        "wind": 12,
        "rain": 20
    }
    notification_count = db_instance.get_collection(
        "notifications"
    ).count_documents({})

    return render_template(
        "dashboard.html",
        stats=stats,
        weather=weather,
        ai_tip=ai_tip,
        crop_predictions=crop_predictions,
        disease_reports=disease_reports,
        notification_count=notification_count
    )

@dashboard_bp.route("/api/dashboard-stats")
@login_required
def api_stats():

    stats = {

    "farmers": db_instance.get_collection("farmers").count_documents({}),

    "lands": db_instance.get_collection("lands").count_documents({}),

    "crops": db_instance.get_collection("crop_predictions").count_documents({}),

    "diseases": db_instance.get_collection("disease_reports").count_documents({}),

    "soil": db_instance.get_collection("soil_reports").count_documents({}),

    "fertilizer": db_instance.get_collection("fertilizer_reports").count_documents({}),

    "irrigation": db_instance.get_collection("irrigation_reports").count_documents({}),

    "yield": db_instance.get_collection("yield_predictions").count_documents({})
}

    return jsonify(stats)


@dashboard_bp.route("/chatbot")
@login_required
def chatbot():
    return render_template("chatbot.html")