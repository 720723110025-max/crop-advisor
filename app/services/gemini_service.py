import os
import google.generativeai as genai

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")

def ask_farmer(question):

    prompt = f"""
You are an agricultural expert.

Answer simply and practically.

Farmer Question:
{question}
"""

    response = model.generate_content(prompt)

    return response.text