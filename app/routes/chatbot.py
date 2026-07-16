from flask import Blueprint, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

chatbot_bp = Blueprint(
    "chatbot",
    __name__,
    url_prefix="/chatbot"
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


@chatbot_bp.route("/")
def index():
    return render_template("chatbot.html")


@chatbot_bp.route("/ask", methods=["POST"])
def ask():

    prompt = f"""
You are an expert agricultural AI assistant.

Answer only agriculture-related questions.

Reply only in {language}.

If the question is not related to agriculture,
politely say:
"I can only answer agriculture-related questions."

Question:
{question}
"""

    try:
        response = model.generate_content(prompt)

        return jsonify({
            "success": True,
            "reply": response.text
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "reply": str(e)
        }), 500