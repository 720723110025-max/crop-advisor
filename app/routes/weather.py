"""
Weather routes for weather advisory.
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.services.weather_service import WeatherService

weather_bp = Blueprint('weather', __name__)

@weather_bp.route('/advisory')
@login_required
def advisory():
    location = request.args.get('location', current_user.farm_location or 'New York')
    weather_service = WeatherService()
    current_weather = weather_service.get_current_weather(location)
    forecast = weather_service.get_forecast(location)
    recommendations = weather_service.get_farming_recommendations(current_weather)
    
    return render_template('weather.html',
                         current_weather=current_weather,
                         forecast=forecast,
                         recommendations=recommendations,
                         location=location)

@weather_bp.route('/api/current-weather')
@login_required
def api_current_weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    location = request.args.get('location')
    
    weather_service = WeatherService()
    
    if lat and lon:
        data = weather_service.get_current_weather(location=None, lat=lat, lon=lon)
    else:
        if not location:
            location = current_user.farm_location or 'New York'
        data = weather_service.get_current_weather(location)
        
    return jsonify(data)

@weather_bp.route('/api/forecast')
@login_required
def api_forecast():
    location = request.args.get('location')
    days = int(request.args.get('days', 5))
    if not location:
        location = current_user.farm_location or 'New York'
    weather_service = WeatherService()
    forecast = weather_service.get_forecast(location, days)
    return jsonify(forecast)

@weather_bp.route('/api/recommendations')
@login_required
def api_recommendations():
    location = request.args.get('location')
    if not location:
        location = current_user.farm_location or 'New York'
    weather_service = WeatherService()
    current_weather = weather_service.get_current_weather(location)
    recommendations = weather_service.get_farming_recommendations(current_weather)
    return jsonify(recommendations)