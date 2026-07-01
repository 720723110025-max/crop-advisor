"""
Disease detection routes for crop disease identification.
Supports camera capture and file upload (PNG/JPG/JPEG).
"""

import os
import uuid
from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from app.utils.database import db_instance
from datetime import datetime
from werkzeug.utils import secure_filename

disease_bp = Blueprint('disease', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
    return (
        '.' in filename
        and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@disease_bp.route('/detect')
@login_required
def detect():
    return render_template('disease_detection.html')


@disease_bp.route('/api/detect-disease', methods=['POST'])
@login_required
def detect_disease():
    try:
        # Support both file upload and base64 camera capture
        image_source = request.form.get('image_source', 'upload')

        if image_source == 'camera':
            # Base64 image from camera
            import base64
            import io
            from PIL import Image as PILImage

            b64_data = request.form.get('image_data', '')
            if not b64_data:
                return jsonify({'error': 'No camera image data received'}), 400

            # Strip data-URL prefix if present
            if ',' in b64_data:
                b64_data = b64_data.split(',', 1)[1]

            image_bytes = base64.b64decode(b64_data)
            img = PILImage.open(io.BytesIO(image_bytes)).convert('RGB')
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
            os.makedirs(upload_folder, exist_ok=True)
            unique_filename = f"{uuid.uuid4().hex}_camera.jpg"
            upload_path = os.path.join(upload_folder, unique_filename)
            img.save(upload_path, 'JPEG')
        else:
            # File upload
            if 'leaf_image' not in request.files:
                return jsonify({'error': 'No file uploaded'}), 400

            file = request.files['leaf_image']
            if file.filename == '':
                return jsonify({'error': 'No file selected'}), 400

            if not allowed_file(file.filename):
                return jsonify({
                    'error': 'Invalid file type. Please upload PNG, JPG, or JPEG.'
                }), 400

            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
            os.makedirs(upload_folder, exist_ok=True)
            upload_path = os.path.join(upload_folder, unique_filename)
            file.save(upload_path)

        crop_type = request.form.get('crop_type', 'Unknown')

        # Run disease detection (with ML or fallback)
        result = _run_detection(upload_path, crop_type)

        # Save to MongoDB
        try:
            report_data = {
                'user_id': current_user.id,
                'image_path': upload_path,
                'image_filename': unique_filename,
                'crop_type': crop_type,
                'disease_name': result['name'],
                'confidence': result['confidence'],
                'severity': result['severity'],
                'symptoms': result['symptoms'],
                'causes': result['causes'],
                'prevention': result['prevention'],
                'treatment': result['treatment'],
                'is_verified': False,
                'created_at': datetime.utcnow(),
            }
            db_instance.get_collection('disease_reports').insert_one(report_data)
        except Exception:
            pass

        return jsonify({
            'success': True,
            'disease': result['name'],
            'confidence': result['confidence'],
            'severity': result['severity'],
            'symptoms': result['symptoms'],
            'causes': result['causes'],
            'prevention': result['prevention'],
            'treatment': result['treatment'],
            'image_path': unique_filename,
        })

    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500


def _run_detection(image_path, crop_type):
    """Try ML model; fall back to rule-based detection."""
    try:
        import cv2
        import numpy as np
        from app.services.ml_models import MLService
        ml = MLService()

        image_array = cv2.imread(image_path)
        if image_array is not None:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
            image_array = cv2.resize(image_array, (100, 100))
            image_array = image_array.astype(np.float32) / 255.0

            if ml.disease_model is not None:
                pred = ml.disease_model.predict(np.expand_dims(image_array, 0))
                # Map to disease names — placeholder labels
                labels = [
                           "Bacterial Leaf Blight",
                           "Brown Spot",
                           "Healthy Rice Leaf",
                           "Leaf Blast",
                           "Leaf scald",
                           "Sheath Blight"
                        ]
                idx = int(np.argmax(pred))
                label = labels[idx] if idx < len(labels) else 'Unknown'
                confidence = float(np.max(pred))
                return {
                    'name': label,
                    'confidence': round(confidence, 2),
                    'severity': 'None' if label == 'Healthy' else 'Moderate',
                    'symptoms': 'See agronomist for detailed assessment',
                    'causes': 'Detected by AI model',
                    'prevention': 'Maintain good crop hygiene',
                    'treatment': 'Consult local extension services',
                }
    except Exception:
        pass

    # Fallback — rule-based / random
    from app.services.ml_models import MLService
    return MLService().detect_disease_fallback(None, crop_type)


@disease_bp.route('/reports')
@login_required
def reports():
    diseases_col = db_instance.get_collection('disease_reports')
    disease_list = list(
        diseases_col.find({'user_id': current_user.id}).sort('created_at', -1)
    )
    return render_template('disease_reports.html', reports=disease_list)
