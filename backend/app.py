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
        # ✅ FIX 2: "gemini-1.5-pro-latest" is also deprecated for many API keys.
        # We are now using "gemini-2.5-flash-preview-09-2025", which is a current
        # and recommended model for this API.
        model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")


        response = model.generate_content(user_message)

        if hasattr(response, "text") and response.text:
            reply = response.text
        else:
            # This can happen if the content is blocked by safety settings
            reply = "🤖 I couldn't generate a proper reply. This might be due to safety settings or other issues. Try again with a different prompt."

        return jsonify({"reply": reply})

    except Exception as e:
        # Log the full error to your console for debugging
        print(f"An error occurred: {e}")
        return jsonify({"reply": f"⚠️ Error contacting Gemini API: {str(e)}"})

@app.route("/")
def home():
    return "🤖 Google Gemini Chatbot Backend running successfully!"

if __name__ == "__main__":
    # It's generally better to use a proper WSGI server like gunicorn for production,
    # but app.run() is fine for testing.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
