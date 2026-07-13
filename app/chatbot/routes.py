from flask import Blueprint, render_template, request, jsonify

chatbot_bp = Blueprint(
    "chatbot",
    __name__,
    url_prefix="/chatbot"
)


@chatbot_bp.route("/")
def index():
    return render_template("chatbot.html")


@chatbot_bp.route("/ask", methods=["POST"])
def ask():

    message = request.form.get("message", "").lower()

    if "rice" in message:
        reply = "Rice grows best in warm temperatures with sufficient water."

    elif "maize" in message:
        reply = "Maize requires well-drained soil and moderate rainfall."

    elif "fertilizer" in message:
        reply = "Use fertilizer based on your soil test results."

    elif "weather" in message:
        reply = "Check the Weather module for the latest advisory."

    else:
        reply = "Sorry, I don't understand. Please ask about crops, weather, fertilizers, or diseases."

    return jsonify({
        "reply": reply
    })