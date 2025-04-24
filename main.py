
import os
from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv

# Optional: Load .env variables locally
load_dotenv()

# Set OpenAI key the old way (works with openai==1.2.4)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Init Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "🤖 HAL is standing by (openai==1.2.4)."

@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "").strip()

        if not question:
            return jsonify({"error": "No question provided."}), 400

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}],
            temperature=0.7
        )

        return jsonify({
            "answer": response["choices"][0]["message"]["content"].strip()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
