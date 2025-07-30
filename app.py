from flask import Flask, render_template, request, jsonify
import logging
import requests
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Use environment variable for API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Fallback (optional, for local testing only — not recommended in production)
if not GEMINI_API_KEY:
    GEMINI_API_KEY = ""  # ← Paste your Gemini API key here to run

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    if not user_input:
        return jsonify({"reply": "I'm here to listen. Please share your thoughts."}), 200

    try:
        response = requests.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{
                    "parts": [{
                        "text": (
                            "You are a chat bot which deals with mental health issues. "
                            "Provide helpful and supportive replies.\n\n"
                            f"User Input: {user_input}"
                        )
                    }]
                }]
            }
        )

        logging.debug(f"Gemini API response: {response.text}")
        response_data = response.json()

        choices = response_data.get("candidates", [])
        if choices:
            reply = choices[0].get("content", {}).get("parts", [])[0].get("text", "").strip()
        else:
            reply = "I'm here for you. Can you tell me more about how you're feeling?"

        if not reply:
            reply = "I'm here for you. Can you tell me more about how you're feeling?"

        return jsonify({"reply": reply})

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error: {e}")
        return jsonify({"reply": "I'm sorry, I encountered an error while processing your request. Please try again later."}), 500
    except Exception as e:
        logging.error(f"General error: {e}")
        return jsonify({"reply": "I'm sorry, I encountered an error while processing your request. Please try again later."}), 500

if __name__ == "__main__":
    app.run(debug=True)
