"""
Crop Recommendation Routes
"""

from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime

from app.services.crop_service import predict_crop as predict_crop_service
from app.utils.database import db_instance
from app.utils.logger import logger

crop_bp = Blueprint("crop", __name__)


@crop_bp.route("/recommend")
@login_required
def recommend():
    return render_template("crop_recommendation.html")


@crop_bp.route("/api/predict-crop", methods=["POST"])
@login_required
def predict_crop():

    try:

        nitrogen = float(request.form.get("nitrogen", 0))
        phosphorus = float(request.form.get("phosphorus", 0))
        potassium = float(request.form.get("potassium", 0))
        temperature = float(request.form.get("temperature", 0))
        humidity = float(request.form.get("humidity", 0))
        ph = float(request.form.get("ph", 7))
        rainfall = float(request.form.get("rainfall", 0))

        result = predict_crop_service(
            nitrogen,
            phosphorus,
            potassium,
            temperature,
            humidity,
            ph,
            rainfall
        )

        if not result["success"]:
            return jsonify(result), 500

        crop = result["crop"]
        confidence = result["confidence"]

        all_recommendations = [
            {
                "crop": crop,
                "confidence": confidence
            }
        ]

        logger.info(
            f"{current_user.username} predicted {crop}"
        )

        seed_info = get_seed_info(crop)
        profit_info = get_profit_info(crop)

        try:

            db_instance.get_collection(
                "crop_predictions"
            ).insert_one({

                "user_id": str(current_user.id),

                "recommended_crop": crop,

                "nitrogen": nitrogen,

                "phosphorus": phosphorus,

                "potassium": potassium,

                "temperature": temperature,

                "humidity": humidity,

                "ph": ph,

                "rainfall": rainfall,

                "confidence": confidence,

                "created_at": datetime.utcnow()

            })

        except Exception:
            pass

        suggestions = []

        if nitrogen < 50:
            suggestions.append("Apply Nitrogen fertilizer.")

        if phosphorus < 40:
            suggestions.append("Apply Phosphorus fertilizer.")

        if potassium < 40:
            suggestions.append("Apply Potassium fertilizer.")

        if rainfall < 100:
            suggestions.append("Provide additional irrigation.")

        if ph < 6:
            suggestions.append("Apply agricultural lime.")

        if ph > 8:
            suggestions.append("Apply organic compost.")

        if not suggestions:
            suggestions.append("Your soil is suitable for cultivation.")

        return jsonify({
            "success": True,
            "crop": crop,
            "confidence": float(confidence),
            "suggestions": suggestions,
            "all_recommendations": all_recommendations,
            "seed_info": seed_info,
            "profit_info": profit_info
        })

    except Exception as e:

        logger.error(f"Crop Prediction Error: {str(e)}")

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

def get_seed_info(crop):
    """
    Return seed information for the recommended crop.
    """

    seeds = {

        "Rice": {
            "varieties": [
                "ADT-43",
                "CO-51",
                "CR-1009"
            ],
            "season": "Kharif",
            "duration": "120 Days",
            "yield": "6.5 Tons / Hectare"
        },

        "Maize": {
            "varieties": [
                "COH(M)-6",
                "NK-6240"
            ],
            "season": "Rabi",
            "duration": "100 Days",
            "yield": "5 Tons / Hectare"
        },

        "Wheat": {
            "varieties": [
                "HD-2967",
                "PBW-343"
            ],
            "season": "Rabi",
            "duration": "130 Days",
            "yield": "4 Tons / Hectare"
        },

        "Cotton": {
            "varieties": [
                "Suraj",
                "Bunny Bt",
                "RCH-659"
            ],
            "season": "Kharif",
            "duration": "160 Days",
            "yield": "2 Tons / Hectare"
        },

        "Sugarcane": {
            "varieties": [
                "CO-86032",
                "COC-671"
            ],
            "season": "Annual",
            "duration": "12 Months",
            "yield": "90 Tons / Hectare"
        }

    }

    return seeds.get(

        crop,

        {
            "varieties": ["Local Variety"],
            "season": "Unknown",
            "duration": "Unknown",
            "yield": "Unknown"
        }

    )

def get_profit_info(crop):
    """
    Return estimated profit details.
    """

    profits = {

        "Rice": {
            "cost": "₹25,000 / Acre",
            "yield": "6.5 Tons",
            "market_price": "₹2,400 / Quintal",
            "profit": "₹60,000"
        },

        "Maize": {
            "cost": "₹18,000 / Acre",
            "yield": "5 Tons",
            "market_price": "₹2,000 / Quintal",
            "profit": "₹45,000"
        },

        "Wheat": {
            "cost": "₹20,000 / Acre",
            "yield": "4 Tons",
            "market_price": "₹2,200 / Quintal",
            "profit": "₹42,000"
        },

        "Cotton": {
            "cost": "₹35,000 / Acre",
            "yield": "2 Tons",
            "market_price": "₹7,500 / Quintal",
            "profit": "₹85,000"
        },

        "Sugarcane": {
            "cost": "₹45,000 / Acre",
            "yield": "90 Tons",
            "market_price": "₹350 / Quintal",
            "profit": "₹1,20,000"
        }

    }

    return profits.get(
        crop,
        {
            "cost": "Unknown",
            "yield": "Unknown",
            "market_price": "Unknown",
            "profit": "Unknown"
        }
    )
@crop_bp.route("/history")
@login_required
def history():

    history = list(

        db_instance.get_collection(
            "crop_predictions"
        ).find(

            {
                "user_id": str(current_user.id)
            }

        ).sort(
            "created_at",
            -1
        )

    )

    return render_template(

        "crop_history.html",

        history=history,

        title="Crop Prediction History"

    )