"""
Disease detection routes for crop disease identification.
Supports camera capture and file upload (PNG/JPG/JPEG).
"""

import os
from unittest import result
from unittest import result
import uuid
from flask import Blueprint, render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from app.utils.database import db_instance
from datetime import datetime
from werkzeug.utils import secure_filename
from app.utils.logger import logger
from flask import send_file
from app.services.pdf_service import create_report
from app.services.email_service import send_report

disease_bp = Blueprint('disease', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def allowed_file(filename):
	return (
		'.' in filename
		and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	)

@disease_bp.route("/send-email", methods=["POST"])
@login_required
def send_email():

    email = request.form["email"]

    body = """
Disease Detection Report

Disease : Brown Spot
Confidence : 95%
Treatment : Spray Mancozeb
"""

    send_report(
        email,
        "Disease Report",
        body
    )

    return jsonify({
        "success": True
    })

@disease_bp.route('/detect')
@login_required
def detect():
	return render_template('disease_detection.html')


@disease_bp.route('/api/detect-disease', methods=['POST'])
@login_required
def detect_disease():
    try:
        # Check uploaded file
        if "leaf_image" not in request.files:
            return jsonify({
                "success": False,
                "error": "No image uploaded"
            }), 400

        file = request.files["leaf_image"]

        if file.filename == "":
            return jsonify({
                "success": False,
                "error": "Please select an image"
            }), 400

        if not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "error": "Only PNG, JPG and JPEG files are allowed"
            }), 400

        # Upload folder
        upload_folder = current_app.config.get(
            "UPLOAD_FOLDER",
            "app/static/uploads"
        )
        os.makedirs(upload_folder, exist_ok=True)

        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        upload_path = os.path.join(upload_folder, unique_filename)

        file.save(upload_path)

        crop_type = request.form.get("crop_type", "Unknown")

        # Run AI model
        result = _run_detection(upload_path, crop_type)

        # Save report (optional)
        try:
            report_data = {
                "user_id": current_user.id,
                "image_path": upload_path,
                "image_filename": unique_filename,
                "crop_type": crop_type,
                "disease_name": result["name"],
                "confidence": result["confidence"],
                "severity": result["severity"],
                "symptoms": result["symptoms"],
                "causes": result["causes"],
                "prevention": result["prevention"],
                "treatment": result["treatment"],
                "is_verified": False,
                "created_at": datetime.utcnow()
            }

            db_instance.get_collection(
                "disease_reports"
            ).insert_one(report_data)

            db_instance.get_collection(
                "notifications"
            ).insert_one({
                "message": f"{current_user.username} detected {result['name']}",
                "type": "Disease",
                "created_at": datetime.utcnow()
            })

        except Exception as db_error:
            logger.error(f"Database Error: {db_error}")

        logger.info(
            f"{current_user.username} detected {result['name']} ({result['confidence']:.2f})"
        )

        return jsonify({
            "success": True,
            "disease": result["name"],
            "confidence": result["confidence"],
            "severity": result["severity"],
            "symptoms": result["symptoms"],
            "causes": result["causes"],
            "prevention": result["prevention"],
            "treatment": result["treatment"]
        })

    except Exception as e:
        logger.error(f"Disease Detection Error: {e}")

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


def _run_detection(image_path, crop_type):
	"""Run disease detection using the trained model."""

	try:
		import cv2
		import numpy as np
		from app.services.ml_models import MLService

		ml = MLService()

		image_array = cv2.imread(image_path)

		if image_array is None:
			raise Exception("Unable to read image")

		image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
		image_array = cv2.resize(image_array, (224, 224))
		image_array = image_array.astype(np.float32) / 255.0

		if ml.disease_model is not None:

			prediction = ml.disease_model.predict(
				np.expand_dims(image_array, axis=0),
				verbose=0
			)

			labels = {
				0: {
					"name": "Bacterial Leaf Blight",
					"symptoms": "Yellow stripes on leaf edges.",
					"causes": "Bacterial infection.",
					"prevention": "Use resistant seeds and avoid excess nitrogen.",
					"treatment": "Spray Copper Oxychloride."
				},
				1: {
					"name": "Brown Spot",
					"symptoms": "Brown circular spots on leaves.",
					"causes": "Fungal infection.",
					"prevention": "Balanced fertilizer and proper irrigation.",
					"treatment": "Spray Mancozeb."
				},
				2: {
					"name": "Healthy",
					"symptoms": "No disease detected.",
					"causes": "Healthy crop.",
					"prevention": "Continue good farming practices.",
					"treatment": "No treatment required."
				},
				3: {
					"name": "Leaf Blast",
					"symptoms": "Diamond-shaped lesions on leaves.",
					"causes": "Magnaporthe fungus.",
					"prevention": "Avoid excess nitrogen.",
					"treatment": "Spray Tricyclazole."
				},
				4: {
					"name": "Leaf Scald",
					"symptoms": "Gray lesions with brown margins.",
					"causes": "Fungal disease.",
					"prevention": "Field sanitation.",
					"treatment": "Spray Carbendazim."
				},
				5: {
					"name": "Sheath Blight",
					"symptoms": "Oval lesions on leaf sheath.",
					"causes": "Rhizoctonia fungus.",
					"prevention": "Reduce plant density.",
					"treatment": "Spray Validamycin."
				}
			}

			idx = int(np.argmax(prediction))
			confidence = float(np.max(prediction))

			result = labels.get(idx, {
				"name": "Unknown",
				"symptoms": "Unknown",
				"causes": "Unknown",
				"prevention": "Consult expert",
				"treatment": "Consult expert"
			})

			if confidence >= 0.85:
				severity = "High"
			elif confidence >= 0.60:
				severity = "Medium"
			else:
				severity = "Low"

			return {
				"name": result["name"],
				"confidence": round(confidence, 2),
				"severity": severity,
				"symptoms": result["symptoms"],
				"causes": result["causes"],
				"prevention": result["prevention"],
				"treatment": result["treatment"]
			}

	except Exception as e:
		print("Disease Detection Error:", e)

	from app.services.ml_models import MLService
	return MLService().detect_disease_fallback(None, crop_type)

@disease_bp.route("/download-report")
@login_required
def download_report():

    filename = "disease_report.pdf"

    data = {
        "Disease": "Brown Spot",
        "Confidence": "95%",
        "Severity": "Medium",
        "Treatment": "Spray Mancozeb"
    }

    create_report(
        filename,
        "Disease Detection Report",
        data
    )

    return send_file(
        filename,
        as_attachment=True
    )

@disease_bp.route('/reports')
@login_required
def reports():
	diseases_col = db_instance.get_collection('disease_reports')
	disease_list = list(
		diseases_col.find({'user_id': current_user.id}).sort('created_at', -1)
	)
	return render_template('disease_reports.html', reports=disease_list)

print("Disease Blueprint Loaded")


from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io

@disease_bp.route("/history")
@login_required
def history():

	reports = list(
		db_instance.get_collection("disease_reports")
		.find({"user_id": current_user.id})
		.sort("created_at", -1)
	)

	return render_template(
		"disease_history.html",
		reports=reports
	)
@disease_bp.route("/report/<report_id>")
@login_required
def report(report_id):

	from bson import ObjectId

	report = db_instance.get_collection(
		"disease_reports"
	).find_one({
		"_id": ObjectId(report_id)
	})

	return render_template(
		"disease_report.html",
		report=report
	)