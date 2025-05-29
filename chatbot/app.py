import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print("Loaded Gemini API Key:", GEMINI_API_KEY)  # Debug print
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY

SYSTEM_PROMPT = (
    "You are a smart, empathetic career counselor chatbot designed to help students from Tier-2 and Tier-3 cities in India. "
    "Provide practical, accessible, and encouraging career guidance, considering local challenges, language barriers, and limited resources. "
    "Suggest both traditional and modern career paths, scholarships, online courses, and motivational advice."
)

def get_gemini_response(user_message):
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "role": "user",
                "parts": [{
                    "text": f"{SYSTEM_PROMPT}\n\nUser: {user_message}"
                }]
            }
        ]
    }
    response = requests.post(GEMINI_API_URL, headers=headers, json=data)
    print("Gemini API response:", response.status_code, response.text)  # Debug print
    if response.ok:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return "Sorry, I couldn't process your request right now."

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    bot_reply = get_gemini_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
