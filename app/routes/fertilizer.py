"""
Fertilizer recommendation routes.
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from app.utils.database import db_instance
from datetime import datetime
from app.services.fertilizer_analysis import FertilizerAnalysisService

fertilizer_bp = Blueprint('fertilizer', __name__)

@fertilizer_bp.route('/recommend')
@login_required
def recommend():
    return render_template('fertilizer.html')

@fertilizer_bp.route('/api/recommend-fertilizer', methods=['POST'])
@login_required
def recommend_fertilizer():
    try:
        crop_type = request.form.get('crop_type', '').strip()
        nitrogen = float(request.form.get('nitrogen', 0))
        phosphorus = float(request.form.get('phosphorus', 0))
        potassium = float(request.form.get('potassium', 0))
        ph = float(request.form.get('ph', 7.0))
        organic_matter = float(request.form.get('organic_matter', 0))
        
        if not crop_type:
            return jsonify({'error': 'Crop type is required'}), 400
        
        # Invoke specialized fertilizer analysis service
        service = FertilizerAnalysisService()
        result = service.recommend_fertilizer(crop_type, nitrogen, phosphorus, potassium, ph, organic_matter)
        
        # Save to database
        fert_col = db_instance.get_collection('fertilizer_recommendations')
        fert_data = {
            'user_id': current_user.id,
            'crop_type': crop_type,
            'nitrogen_level': nitrogen,
            'phosphorus_level': phosphorus,
            'potassium_level': potassium,
            'recommended_fertilizer': result['fertilizer_name'],
            'quantity': result['quantity'],
            'unit': result['unit'],
            'application_method': result['application_method'],
            'application_schedule': result['application_schedule'],
            'frequency': result['frequency'],
            'expected_improvement': result['expected_improvement'],
            'created_at': datetime.utcnow()
        }
        fert_col.insert_one(fert_data)
        
        return jsonify({
            'success': True,
            'fertilizer_name': result['fertilizer_name'],
            'quantity': result['quantity'],
            'unit': result['unit'],
            'application_method': result['application_method'],
            'application_schedule': result['application_schedule'],
            'frequency': result['frequency'],
            'expected_improvement': result['expected_improvement']
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@fertilizer_bp.route('/api/history')
@login_required
def api_history():
    try:
        fert_col = db_instance.get_collection('fertilizer_recommendations')
        history = list(fert_col.find({'user_id': current_user.id}).sort('created_at', -1).limit(10))
        
        serialized = []
        for item in history:
            serialized.append({
                'created_at': item.get('created_at').isoformat() if item.get('created_at') else None,
                'crop_type': item.get('crop_type', ''),
                'fertilizer': item.get('recommended_fertilizer', ''),
                'quantity': item.get('quantity', 0),
                'unit': item.get('unit', 'kg/ha')
            })
        return jsonify(serialized)
    except Exception as e:
        return jsonify({'error': str(e)}), 500