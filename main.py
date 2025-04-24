
import os
from flask import Flask, request, jsonify
import openai

# Set OpenAI key (openai==1.2.4 style)
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Init Flask
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "🤖 HAL is standing by (no dotenv)."

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
