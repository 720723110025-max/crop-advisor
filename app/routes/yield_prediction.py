"""
Yield prediction routes.
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.utils.database import db_instance
from datetime import datetime

yield_bp = Blueprint('yield', __name__)

MARKET_PRICE = {
    'rice': 22000,
    'wheat': 25000,
    'maize': 18000,
    'sugarcane': 35000,
    'cotton': 60000,
    'vegetables': 30000,
}

BASE_YIELD = {
    'rice': 4.5,
    'wheat': 3.5,
    'maize': 5.0,
    'sugarcane': 6.0,
    'cotton': 2.5,
    'vegetables': 5.5,
}


@yield_bp.route('/predict')
@login_required
def predict():
    return render_template('yield_prediction.html')


@yield_bp.route('/api/predict-yield', methods=['POST'])
@login_required
def predict_yield():
    try:
        crop_type = request.form.get('crop_type', '').strip()
        area = float(request.form.get('area', 0))
        soil_quality = float(request.form.get('soil_quality', 0))
        temperature = float(request.form.get('temperature', 25))
        rainfall = float(request.form.get('rainfall', 0))
        fertilizer_used = float(request.form.get('fertilizer_used', 0))

        if not crop_type or area <= 0:
            return jsonify({'error': 'Valid crop type and area are required'}), 400

        base = BASE_YIELD.get(crop_type.lower(), 4.0)
        soil_factor = 0.5 + (soil_quality / 100)
        temp_factor = 1 - abs(temperature - 25) / 50
        rain_factor = 1 - abs(rainfall - 200) / 300

        predicted_yield = base * soil_factor * max(0.5, temp_factor) * max(0.5, rain_factor)
        confidence = 0.7 + (soil_quality / 500) + (0.05 if 20 <= temperature <= 30 else 0)
        confidence = min(0.95, max(0.5, confidence))

        price = MARKET_PRICE.get(crop_type.lower(), 20000)
        income = round(predicted_yield * area * price, 2)

        # Save prediction to database
        yield_col = db_instance.get_collection('yield_predictions')
        pred_data = {
            'user_id': current_user.id,
            'crop_type': crop_type,
            'area': area,
            'soil_quality': soil_quality,
            'weather_conditions': f"Temp: {temperature}°C, Rainfall: {rainfall}mm",
            'predicted_yield': round(predicted_yield, 2),
            'confidence_score': confidence,
            'estimated_income': income,
            'factors': 'Soil quality, temperature, and rainfall',
            'recommendations': [
                'Maintain soil pH between 6.5 and 7.5',
                'Apply recommended fertilizers on schedule',
                'Ensure proper irrigation',
                'Monitor weather conditions regularly',
            ],
            'created_at': datetime.utcnow(),
        }
        yield_col.insert_one(pred_data)

        return jsonify({
            'success': True,
            'yield': round(predicted_yield, 2),
            'income': income,
            'unit': 'tons/acre',
            'confidence': confidence,
            'area': area,
            'factors': 'Soil quality, temperature, and rainfall are key factors',
            'recommendations': '\n'.join(pred_data['recommendations']),
        })

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


@yield_bp.route('/api/yield-history')
@login_required
def api_history():
    yield_col = db_instance.get_collection('yield_predictions')
    history = list(yield_col.find(
        {'user_id': current_user.id},
    ).sort('created_at', -1).limit(10))
    # Convert ObjectId to string for JSON
    for h in history:
        h['_id'] = str(h['_id'])
        if 'created_at' in h:
            h['created_at'] = h['created_at'].isoformat()
    return jsonify({'success': True, 'history': history})


@yield_bp.route('/api/yield-visualization')
@login_required
def yield_visualization():
    return jsonify({
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'predicted': [4.2, 4.5, 4.8, 5.0, 4.7, 4.3],
        'actual': [4.0, 4.3, 4.6, 4.9, 4.5, 4.1],
    })
