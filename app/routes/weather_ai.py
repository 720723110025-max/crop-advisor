from flask import Blueprint, request, jsonify

weather_ai_bp = Blueprint(
    "weather_ai",
    __name__,
    url_prefix="/weather-ai"
)

@weather_ai_bp.route("/advice", methods=["POST"])
def advice():

    temperature = float(request.form["temperature"])
    humidity = float(request.form["humidity"])
    rainfall = float(request.form["rainfall"])

    advice = []

    if rainfall > 120:
        advice.append("Heavy rain expected. Avoid irrigation.")

    elif rainfall < 30:
        advice.append("Low rainfall. Irrigate your crops.")

    if temperature > 35:
        advice.append("High temperature. Water crops in the morning or evening.")

    if humidity > 80:
        advice.append("High humidity. Monitor crops for fungal diseases.")

    if not advice:
        advice.append("Weather conditions are suitable for farming.")

    return jsonify({
        "advice": advice
    })