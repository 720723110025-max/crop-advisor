from flask import Blueprint, render_template, request, jsonify

chatbot_bp = Blueprint(
    "chatbot",
    __name__,
    url_prefix="/chatbot"
)


@chatbot_bp.route("/")
def index():
    return render_template("chatbot/index.html")


@chatbot_bp.route("/ask", methods=["POST"])
def ask():

    question = request.form.get("message", "").lower()

    answer = "Sorry, I don't understand."

    if "rice" in question or "paddy" in question:
        answer = "Paddy grows well in loamy soil with adequate water."

    elif "soil" in question:
        answer = "Loamy soil is suitable for most crops."

    elif "fertilizer" in question:
        answer = "Use NPK fertilizer according to soil test."

    elif "weather" in question:
        answer = "Today's weather is cloudy with chances of rain."

    elif "market" in question:
        answer = "Today's paddy market price is ₹2450 per quintal."

    return jsonify({

        "question": question,

        "answer": answer

    })