"""
Gemini AI Service
"""

import os

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

# Load Model
model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def ask_gemini(question):
    """
    General AI Assistant
    """

    prompt = f"""
You are an expert agricultural assistant.

Answer the following farmer question clearly.

Question:
{question}

Rules:
- Keep the answer practical.
- Maximum 150 words.
- Mention crops, fertilizer, irrigation, disease or weather whenever relevant.
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception as e:

        return f"Gemini Error: {e}"


def get_ai_tip(weather):
    """
    Weather-based AI Tip
    """

    prompt = f"""
You are an agriculture expert.

Weather

Temperature : {weather.get("temperature")}

Humidity : {weather.get("humidity")}

Condition : {weather.get("condition")}

Wind : {weather.get("wind")}

Rain : {weather.get("rain")}

Give one farming recommendation.
Maximum 50 words.
"""

    try:

        response = model.generate_content(prompt)

        return response.text

    except Exception:

        return "Weather is suitable for normal farming activities."