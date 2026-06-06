from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

app = Flask(__name__)

DEFAULT_SYSTEM_PROMPT = (
    "You are a helpful, friendly AI assistant. "
    "Answer clearly, keep responses concise, and ask follow-up questions when useful."
)
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", DEFAULT_SYSTEM_PROMPT)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

conversation_history = [{"role": "system", "content": SYSTEM_PROMPT}]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat_route():
    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    if not os.getenv("OPENROUTER_API_KEY"):
        return jsonify({"error": "OPENROUTER_API_KEY is not set on the server."}), 500

    conversation_history.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="openrouter/auto",
        messages=conversation_history
    )

    reply = response.choices[0].message.content
    conversation_history.append({"role": "assistant", "content": reply})

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)