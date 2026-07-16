import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None


def get_ai_tip(weather):

    if model is None:
        return "Gemini API key is not configured."

    prompt = f"""
You are an Agriculture Expert.

Weather:
Temperature : {weather.get('temperature', 'N/A')}°C
Humidity : {weather.get('humidity', 'N/A')}%
Condition : {weather.get('condition', 'N/A')}
Wind : {weather.get('wind', 'N/A')} km/h
Rain : {weather.get('rain', 'N/A')}%

Give one short farming recommendation.
Maximum 40 words.
"""

    try:
        response = model.generate_content(prompt)
        return response.text

    except Exception:
        return "Weather is suitable for normal farming activities."