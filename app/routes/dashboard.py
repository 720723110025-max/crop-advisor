"""
Dashboard routes for the main application dashboard.
"""

from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user

from app.utils.database import db_instance
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    # Get counts for overview cards
    users_col = db_instance.get_collection('users')
    soil_col = db_instance.get_collection('soil_data')
    disease_col = db_instance.get_collection('disease_reports')
    fertilizer_col = db_instance.get_collection('fertilizer_recommendations')
    irrigation_col = db_instance.get_collection('irrigation_schedules')
    yield_col = db_instance.get_collection('yield_predictions')
    
    stats = {
        'total_soil_tests': soil_col.count_documents({'user_id': current_user.id}),
        'total_disease_reports': disease_col.count_documents({'user_id': current_user.id}),
        'total_fertilizer_recommendations': fertilizer_col.count_documents({'user_id': current_user.id}),
        'total_irrigation_schedules': irrigation_col.count_documents({'user_id': current_user.id}),
        'total_yield_predictions': yield_col.count_documents({'user_id': current_user.id}),
        'pending_tasks': irrigation_col.count_documents({
            'user_id': current_user.id,
            'is_completed': False
        })
    }
    
    # Get recent data
    recent_soil = list(soil_col.find({'user_id': current_user.id})
                      .sort('created_at', -1).limit(5))
    recent_disease = list(disease_col.find({'user_id': current_user.id})
                         .sort('created_at', -1).limit(5))
    recent_fertilizer = list(fertilizer_col.find({'user_id': current_user.id})
                            .sort('created_at', -1).limit(5))
    recent_irrigation = list(irrigation_col.find({'user_id': current_user.id})
                            .sort('irrigation_timing', -1).limit(5))
    recent_yield = list(yield_col.find({'user_id': current_user.id})
                       .sort('created_at', -1).limit(5))
    
    # Get weather data
    weather_data = None
    if current_user.farm_location:
        weather_data = {
            'temperature': 25,
            'humidity': 65,
            'condition': 'Partly Cloudy',
            'wind_speed': 12,
            'pressure': 1015
        }
    
    crop_recommendations = [
        {'crop': 'Rice', 'confidence': 0.92, 'season': 'Kharif'},
        {'crop': 'Wheat', 'confidence': 0.87, 'season': 'Rabi'},
        {'crop': 'Maize', 'confidence': 0.83, 'season': 'Kharif'}
    ]
    
    disease_alerts = list(disease_col.find({
        'user_id': current_user.id,
        'is_verified': True
    }).sort('created_at', -1).limit(3))
    
    irrigation_alerts = list(irrigation_col.find({
        'user_id': current_user.id,
        'is_completed': False
    }).sort('irrigation_timing', 1).limit(3))
    
    return render_template('dashboard.html',
                         stats=stats,
                         weather_data=weather_data,
                         crop_recommendations=crop_recommendations,
                         disease_alerts=disease_alerts,
                         irrigation_alerts=irrigation_alerts,
                         recent_soil_data=recent_soil,
                         recent_disease_reports=recent_disease,
                         recent_fertilizer=recent_fertilizer,
                         recent_irrigation=recent_irrigation,
                         recent_yield=recent_yield,
                         now=datetime.utcnow())

@dashboard_bp.route('/api/dashboard-stats')
@login_required
def api_stats():
    soil_col = db_instance.get_collection('soil_data')
    disease_col = db_instance.get_collection('disease_reports')
    fertilizer_col = db_instance.get_collection('fertilizer_recommendations')
    irrigation_col = db_instance.get_collection('irrigation_schedules')
    yield_col = db_instance.get_collection('yield_predictions')
    
    stats = {
        'soil_tests': soil_col.count_documents({'user_id': current_user.id}),
        'disease_reports': disease_col.count_documents({'user_id': current_user.id}),
        'fertilizer_recommendations': fertilizer_col.count_documents({'user_id': current_user.id}),
        'irrigation_schedules': irrigation_col.count_documents({'user_id': current_user.id}),
        'yield_predictions': yield_col.count_documents({'user_id': current_user.id}),
        'pending_irrigation': irrigation_col.count_documents({
            'user_id': current_user.id,
            'is_completed': False
        })
    }
    return jsonify(stats)
