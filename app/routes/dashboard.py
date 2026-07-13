"""
Dashboard routes for the main application dashboard.
"""

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from app.utils.database import db_instance

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
        crop_predictions=crop_predictions,
        disease_reports=disease_reports,
        weather=weather,
        notification_count=notification_count
    )

@dashboard_bp.route("/api/dashboard-stats")
@login_required
def api_stats():

    stats = {
        "farmers": db_instance.get_collection("farmers").count_documents({}),
        "lands": db_instance.get_collection("lands").count_documents({}),
        "crops": db_instance.get_collection("crop_predictions").count_documents({}),
        "diseases": db_instance.get_collection("disease_reports").count_documents({})
    }

    return jsonify(stats)


@dashboard_bp.route("/chatbot")
@login_required
def chatbot():
    return render_template("chatbot.html")