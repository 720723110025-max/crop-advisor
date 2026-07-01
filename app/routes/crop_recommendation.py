"""
Crop recommendation routes.
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.utils.database import db_instance
from datetime import datetime

crop_bp = Blueprint('crop', __name__)


@crop_bp.route('/recommend')
@login_required
def recommend():
    return render_template('crop_recommendation.html')


@crop_bp.route('/api/predict-crop', methods=['POST'])
@login_required
def predict_crop():
    try:
        nitrogen = float(request.form.get('nitrogen', 0))
        phosphorus = float(request.form.get('phosphorus', 0))
        potassium = float(request.form.get('potassium', 0))
        temperature = float(request.form.get('temperature', 0))
        humidity = float(request.form.get('humidity', 0))
        ph = float(request.form.get('ph', 7.0))
        rainfall = float(request.form.get('rainfall', 0))

        # Try ML model first; fall back to rule-based
        crop, confidence, all_recommendations = _predict(
            nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall
        )

        # Save to database
        try:
            rec_data = {
                'user_id': str(current_user.id),
                'crop': crop,
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'potassium': potassium,
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph,
                'rainfall': rainfall,
                'confidence': confidence,
                'created_at': datetime.utcnow(),
            }
            db_instance.get_collection('crop_recommendations').insert_one(rec_data)
        except Exception:
            pass  # DB error should not break the response

        return jsonify({
            'success': True,
            'crop': crop,
            'confidence': confidence,
            'suggestions': (
                'Use certified quality seeds\n'
                'Maintain proper irrigation\n'
                'Apply fertilizers as recommended by soil test'
            ),
            'all_recommendations': all_recommendations,
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


def _predict(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
    """Try sklearn model, fall back to simple rules."""
    try:
        from app.services.ml_models import MLService
        ml = MLService()
        features = [nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]
        result = ml.predict_crop(features)
        if result.get('success'):
            recs = result.get('recommendations', [])
            return result['crop'], result['confidence'], recs
    except Exception:
        pass

    # Rule-based fallback
    if temperature > 30 and humidity > 80 and rainfall > 200:
        crop, confidence = 'Rice', 0.92
    elif temperature > 25 and humidity > 60:
        crop, confidence = 'Maize', 0.87
    elif temperature < 25:
        crop, confidence = 'Wheat', 0.85
    else:
        crop, confidence = 'Vegetables', 0.75

    all_recs = [
        {'crop': crop, 'confidence': confidence},
        {'crop': 'Maize', 'confidence': 0.85},
        {'crop': 'Wheat', 'confidence': 0.80},
    ]
    return crop, confidence, all_recs
