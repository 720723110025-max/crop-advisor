from flask import Blueprint, render_template, request, jsonify
import joblib
import pandas as pd

fertilizer_bp = Blueprint(
    "fertilizer",
    __name__,
    url_prefix="/fertilizer"
)

# Load trained model
fertilizer_model = joblib.load("models/fertilizer_model.pkl")


@fertilizer_bp.route("/")
def index():
    return render_template("fertilizer.html")


@fertilizer_bp.route("/api/recommend-fertilizer", methods=["POST"])
def recommend_fertilizer():

    try:

        crop = request.form["crop_type"]

        organic = float(request.form["organic_matter"])

        nitrogen = float(request.form["nitrogen"])

        phosphorus = float(request.form["phosphorus"])

        potassium = float(request.form["potassium"])

        ph = float(request.form["ph"])

        # Dummy values because the dataset requires them
        sample = pd.DataFrame([{
            "Temparature": 30,
            "Humidity ": 60,
            "Moisture": organic,
            "Soil Type": "Loamy",
            "Crop Type": crop,
            "Nitrogen": nitrogen,
            "Potassium": potassium,
            "Phosphorous": phosphorus
        }])

        fertilizer = fertilizer_model.predict(sample)[0]

        return jsonify({

            "success": True,

            "fertilizer_name": fertilizer,

            "quantity": "50",

            "unit": "kg/acre",

            "application_method": "Apply evenly around the crop.",

            "application_schedule": "Every 30 days",

            "expected_improvement": "Improves crop growth and yield."

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "error": str(e)

        }), 500