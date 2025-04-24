
import os
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Optional: Load .env variables in dev/local
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI client (new-style SDK 1.3.9)
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route("/", methods=["GET"])
def index():
    return "🤖 HAL is online and sassy."

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "No question provided."}), 400

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}],
            temperature=0.7,
        )

        return jsonify({
            "answer": response.choices[0].message.content.strip()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
