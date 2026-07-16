"""
Disease Detection Routes
AI Crop Disease Detection
"""

import os
import uuid
from datetime import datetime
from app.services.excel_service import create_excel

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    current_app,
    send_file
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import secure_filename

from app.utils.database import db_instance
from app.utils.logger import logger

from app.services.email_service import send_report
from app.services.pdf_service import create_report

disease_bp = Blueprint(
    "disease",
    __name__
)

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg"
}


def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


# --------------------------------------------------
# Disease Detection Page
# --------------------------------------------------

@disease_bp.route("/detect")
@login_required
def detect():

    return render_template(
        "disease_detection.html"
    )


# --------------------------------------------------
# Email Report
# --------------------------------------------------

@disease_bp.route(
    "/send-email",
    methods=["POST"]
)
@login_required
def send_email():

    email = request.form.get("email")

    body = """

Crop Disease Detection Report

Disease : Brown Spot

Confidence : 95%

Severity : Medium

Treatment :

Spray Mancozeb

"""

    filename = "disease_report.pdf"

    send_report(

    	email,

    	"AI Crop Disease Report",

    	body,

    	filename

)

    return jsonify({

        "success": True,

        "message": "Email Sent Successfully"

    })


# --------------------------------------------------
# Detect Disease API
# --------------------------------------------------

@disease_bp.route(
    "/api/detect-disease",
    methods=["POST"]
)
@login_required
def detect_disease():

    try:

        if "leaf_image" not in request.files:

            return jsonify({

                "success": False,

                "error": "No Image Uploaded"

            }), 400

        file = request.files["leaf_image"]

        if file.filename == "":

            return jsonify({

                "success": False,

                "error": "Select an Image"

            }), 400

        if not allowed_file(file.filename):

            return jsonify({

                "success": False,

                "error": "Only PNG/JPG/JPEG Allowed"

            }), 400

        upload_folder = current_app.config.get(

            "UPLOAD_FOLDER",

            "app/static/uploads"

        )

        os.makedirs(

            upload_folder,

            exist_ok=True

        )

        filename = secure_filename(file.filename)

        filename = (

            uuid.uuid4().hex

            + "_"

            + filename

        )

        image_path = os.path.join(

            upload_folder,

            filename

        )

        file.save(image_path)

        crop_type = request.form.get(

            "crop_type",

            "Unknown"

        )

        result = _run_detection(

            image_path,

            crop_type

        )
        try:

            report_data = {

                "user_id": str(current_user.id),

                "username": current_user.username,

                "image_path": image_path,

                "image_filename": filename,

                "crop_type": crop_type,

                "disease_name": result["name"],

                "confidence": result["confidence"],

                "severity": result["severity"],

                "symptoms": result["symptoms"],

                "causes": result["causes"],

                "prevention": result["prevention"],

                "treatment": result["treatment"],

                "created_at": datetime.utcnow()

            }

            db_instance.get_collection(
                "disease_reports"
            ).insert_one(report_data)

            db_instance.get_collection(
                "notifications"
            ).insert_one({

                "message":
                f"{current_user.username} detected {result['name']}",

                "type": "Disease",

                "created_at": datetime.utcnow()

            })

        except Exception as db_error:

            logger.error(
                f"Database Error : {db_error}"
            )

        logger.info(

            f"{current_user.username} detected "

            f"{result['name']} "

            f"({result['confidence']}%)"

        )

        return jsonify({

            "success": True,

            "disease": result["name"],

            "confidence": result["confidence"],

            "severity": result["severity"],

            "symptoms": result["symptoms"],

            "causes": result["causes"],

            "prevention": result["prevention"],

            "treatment": result["treatment"],

            "image":

            "/static/uploads/" + filename

        })

    except Exception as e:

        logger.error(

            f"Disease Detection Error : {e}"

        )

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500
    

@disease_bp.route("/export-excel")
@login_required
def export_excel():

    reports = list(

        db_instance.get_collection(
            "disease_reports"
        ).find({

            "user_id": str(current_user.id)

        })

    )

    filename = "disease_reports.xlsx"

    create_excel(

        filename,

        reports

    )

    return send_file(

        filename,

        as_attachment=True

    )


# --------------------------------------------------
# AI Detection Engine
# --------------------------------------------------

def _run_detection(image_path, crop_type):

    try:

        import cv2
        import numpy as np

        from app.services.ml_models import MLService

        ml = MLService()

        image = cv2.imread(image_path)

        if image is None:

            raise Exception(
                "Unable to Read Image"
            )

        image = cv2.cvtColor(

            image,

            cv2.COLOR_BGR2RGB

        )

        image = cv2.resize(

            image,

            (224, 224)

        )

        image = image.astype(

            np.float32

        ) / 255.0

        if ml.disease_model is not None:

            prediction = ml.disease_model.predict(

                np.expand_dims(
                    image,
                    axis=0
                ),

                verbose=0

            )

            confidence = float(

                np.max(prediction)

            )

            index = int(

                np.argmax(prediction)

            )

            labels = {

                0:{

                    "name":"Bacterial Leaf Blight",

                    "symptoms":"Yellow stripes on leaves.",

                    "causes":"Bacterial infection.",

                    "prevention":"Use resistant seeds.",

                    "treatment":"Copper Oxychloride Spray"

                },

                1:{

                    "name":"Brown Spot",

                    "symptoms":"Brown circular spots.",

                    "causes":"Fungal Infection.",

                    "prevention":"Balanced Fertilizer.",

                    "treatment":"Spray Mancozeb"

                },

                2:{

                    "name":"Healthy",

                    "symptoms":"Healthy Leaf",

                    "causes":"None",

                    "prevention":"Continue Good Farming",

                    "treatment":"No Treatment Required"

                },

                3:{

                    "name":"Leaf Blast",

                    "symptoms":"Diamond Lesions",

                    "causes":"Magnaporthe Fungus",

                    "prevention":"Avoid Excess Nitrogen",

                    "treatment":"Spray Tricyclazole"

                }

            }

            disease = labels.get(

                index,

                labels[2]

            )

            if confidence >= 0.85:

                severity = "High"

            elif confidence >= 0.60:

                severity = "Medium"

            else:

                severity = "Low"

            return {

                "name": disease["name"],

                "confidence": round(
                    confidence * 100,
                    2
                ),

                "severity": severity,

                "symptoms": disease["symptoms"],

                "causes": disease["causes"],

                "prevention": disease["prevention"],

                "treatment": disease["treatment"]

            }

    except Exception as e:

        logger.error(

            f"ML Error : {e}"

        )

    from app.services.ml_models import MLService

    return MLService().detect_disease_fallback(

        None,

        crop_type

    )
# --------------------------------------------------
# Download PDF Report
# --------------------------------------------------

@disease_bp.route("/download-report")
@login_required
def download_report():

    report = db_instance.get_collection(
        "disease_reports"
    ).find_one(

        {
            "user_id": str(current_user.id)
        },

        sort=[("created_at", -1)]

    )

    if report is None:

        return "No report available", 404

    filename = "disease_report.pdf"

    data = {

        "Crop": report.get("crop_type", "Unknown"),

        "Disease": report.get("disease_name", "Unknown"),

        "Confidence":
        f"{report.get('confidence',0)}%",

        "Severity":
        report.get("severity","Unknown"),

        "Symptoms":
        report.get("symptoms","Unknown"),

        "Causes":
        report.get("causes","Unknown"),

        "Prevention":
        report.get("prevention","Unknown"),

        "Treatment":
        report.get("treatment","Unknown")

    }

    create_report(

        filename,

        "AI Crop Disease Detection Report",

        data

    )

    return send_file(

        filename,

        as_attachment=True

    )


# --------------------------------------------------
# Disease History
# --------------------------------------------------

@disease_bp.route("/history")
@login_required
def history():

    reports = list(

        db_instance.get_collection(
            "disease_reports"
        ).find({

            "user_id": str(current_user.id)

        }).sort(

            "created_at",

            -1

        )

    )

    return render_template(

        "disease_history.html",

        reports=reports

    )


# --------------------------------------------------
# Single Report
# --------------------------------------------------

@disease_bp.route("/report/<report_id>")
@login_required
def report(report_id):

    from bson import ObjectId

    report = db_instance.get_collection(

        "disease_reports"

    ).find_one({

        "_id": ObjectId(report_id)

    })

    if report is None:

        return render_template(

            "errors/404.html"

        ), 404

    return render_template(

        "disease_report.html",

        report=report

    )


# --------------------------------------------------
# All Reports
# --------------------------------------------------

@disease_bp.route("/reports")
@login_required
def reports():

    reports = list(

        db_instance.get_collection(

            "disease_reports"

        ).find({

            "user_id": str(current_user.id)

        }).sort(

            "created_at",

            -1

        )

    )

    return render_template(

        "disease_reports.html",

        reports=reports

    )


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@disease_bp.route("/status")
def status():

    return jsonify({

        "success": True,

        "module": "Disease Detection",

        "version": "2.0"

    })


print("Disease Blueprint Loaded Successfully")