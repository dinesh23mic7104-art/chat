from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

HF_API_KEY = os.environ.get("HF_API_KEY")
MODEL_URL = "https://router.huggingface.co/hf-inference/models/microsoft/DialoGPT-medium"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)
    user_message = data.get('message', '')
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": user_message}

    try:
        response = requests.post(MODEL_URL, headers=headers, json=payload, timeout=30)
        result = response.json()
        bot_reply = None

        if isinstance(result, dict) and "generated_text" in result:
            bot_reply = result["generated_text"]
        elif isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            bot_reply = result[0]["generated_text"]
        elif isinstance(result, dict) and "outputs" in result:
            outputs = result["outputs"]
            if isinstance(outputs, list) and len(outputs) > 0:
                content = outputs[0].get("content", [])
                if content and isinstance(content, list) and "text" in content[0]:
                    bot_reply = content[0]["text"]

        if not bot_reply:
            bot_reply = result.get("error", "🤖 Model warming up — please retry.")
    except Exception as e:
        bot_reply = f"⚠️ Error contacting AI: {e}"

    return jsonify({"reply": bot_reply})

@app.route('/')
def home():
    return "🤖 Smart Chatbot backend is running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
