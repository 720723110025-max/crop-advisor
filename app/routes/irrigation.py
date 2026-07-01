"""
Irrigation routes for smart irrigation recommendations.
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user

from app.utils.database import db_instance
from datetime import datetime, timedelta
from app.services.irrigation_optimizer import IrrigationOptimizer

irrigation_bp = Blueprint('irrigation', __name__)

@irrigation_bp.route('/schedule')
@login_required
def schedule():
    irrigation_col = db_instance.get_collection('irrigation_schedules')
    upcoming = list(irrigation_col.find({
        'user_id': current_user.id,
        'is_completed': False
    }).sort('irrigation_timing', 1))
    
    completed = list(irrigation_col.find({
        'user_id': current_user.id,
        'is_completed': True
    }).sort('irrigation_timing', -1).limit(10))
    
    return render_template('irrigation.html', upcoming=upcoming, completed=completed)

@irrigation_bp.route('/api/irrigation-advice', methods=['POST'])
@login_required
def irrigation_advice():
    try:
        crop_type = request.form.get('crop_type', '').strip()
        soil_moisture = float(request.form.get('soil_moisture', 0))
        temperature = float(request.form.get('temperature', 25))
        humidity = float(request.form.get('humidity', 60))
        rainfall = float(request.form.get('rainfall', 0))
        
        if not crop_type:
            return jsonify({'error': 'Crop type is required'}), 400
        
        # Invoke specialized irrigation optimizer service
        optimizer = IrrigationOptimizer()
        result = optimizer.get_irrigation_advice(crop_type, soil_moisture, temperature, humidity, rainfall)
        
        needs_irrigation = result['needs_irrigation']
        water_requirement = result['water_requirement']
        timing_hours = result['timing_hours']
        duration = result['duration_hours']
        method = result['method']
        notes = result['notes']
        
        # Save schedule if irrigation is needed
        if needs_irrigation:
            irrigation_col = db_instance.get_collection('irrigation_schedules')
            schedule_data = {
                'user_id': current_user.id,
                'crop_type': crop_type,
                'soil_moisture': soil_moisture,
                'water_requirement': water_requirement,
                'irrigation_timing': datetime.utcnow() + timedelta(hours=timing_hours),
                'duration': duration,
                'method': method,
                'notes': notes,
                'is_completed': False,
                'created_at': datetime.utcnow()
            }
            irrigation_col.insert_one(schedule_data)
        
        return jsonify({
            'success': True,
            'needs_irrigation': needs_irrigation,
            'water_requirement': water_requirement,
            'timing': (datetime.utcnow() + timedelta(hours=timing_hours)).isoformat() if needs_irrigation else None,
            'duration': duration if needs_irrigation else 0,
            'method': method if needs_irrigation else 'None needed',
            'notes': notes
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

@irrigation_bp.route('/api/history')
@login_required
def api_history():
    try:
        irrigation_col = db_instance.get_collection('irrigation_schedules')
        history = list(irrigation_col.find({
            'user_id': current_user.id,
            'is_completed': True
        }).sort('irrigation_timing', -1).limit(10))
        
        serialized = []
        for item in history:
            serialized.append({
                'id': str(item['_id']),
                'crop_type': item.get('crop_type', ''),
                'timing': item.get('irrigation_timing').isoformat() if item.get('irrigation_timing') else None,
                'water_requirement': item.get('water_requirement', 0),
                'method': item.get('method', ''),
                'is_completed': item.get('is_completed', True)
            })
        return jsonify(serialized)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@irrigation_bp.route('/api/upcoming')
@login_required
def api_upcoming():
    try:
        irrigation_col = db_instance.get_collection('irrigation_schedules')
        upcoming = list(irrigation_col.find({
            'user_id': current_user.id,
            'is_completed': False
        }).sort('irrigation_timing', 1))
        
        serialized = []
        for item in upcoming:
            serialized.append({
                'id': str(item['_id']),
                'crop_type': item.get('crop_type', ''),
                'timing': item.get('irrigation_timing').isoformat() if item.get('irrigation_timing') else None,
                'water_requirement': item.get('water_requirement', 0),
                'method': item.get('method', ''),
                'is_completed': item.get('is_completed', False)
            })
        return jsonify(serialized)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@irrigation_bp.route('/api/complete/<string:schedule_id>', methods=['POST'])
@login_required
def complete_irrigation(schedule_id):
    from bson import ObjectId
    try:
        irrigation_col = db_instance.get_collection('irrigation_schedules')
        result = irrigation_col.update_one(
            {'_id': ObjectId(schedule_id), 'user_id': current_user.id},
            {'$set': {'is_completed': True, 'updated_at': datetime.utcnow()}}
        )
        if result.modified_count > 0:
            return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Schedule not found or already completed'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500