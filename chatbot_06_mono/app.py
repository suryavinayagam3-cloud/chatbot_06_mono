import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
app = Flask(__name__)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = "gemini-3.1-flash-lite"

with open("chatbot_config.txt", encoding="utf-8") as file:
    SYSTEM_PROMPT = file.read()

@app.get("/")
def index():
    return render_template("index.html")

@app.post("/chat")
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Please enter a question."}), 400
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=message,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        )
        return jsonify({"reply": response.text})
    except Exception:
        return jsonify({"error": "The chatbot is temporarily unavailable."}), 500

if __name__ == "__main__":
    app.run()
