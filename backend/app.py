from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# Load Gemini API key from environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("⚠️ GEMINI_API_KEY is missing! Please set it in environment variables.")

# Configure Gemini client
genai.configure(api_key=GEMINI_API_KEY)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please enter a message!"})

    try:
        # Using Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(user_message)

        # Extract text from response
        if hasattr(response, "text") and response.text:
            reply = response.text
        else:
            reply = "🤖 I couldn’t generate a proper reply. Try again."

        return jsonify({"reply": reply})

    except Exception as e:
        return jsonify({"reply": f"⚠️ Error contacting Gemini API: {str(e)}"})

@app.route("/")
def home():
    return "🤖 Google Gemini Chatbot Backend running successfully!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
