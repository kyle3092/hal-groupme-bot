
import os
from flask import Flask, request, jsonify
import openai

# Set OpenAI key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Init Flask
app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def root():
    if request.method == "GET":
        return "🤖 HAL is standing by."

    # GroupMe bot webhook logic
    data = request.get_json()
    message = data.get("text", "").strip()

    if message.lower().startswith("bootup hal:"):
        prompt = message[len("bootup hal:"):].strip()
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            reply = response["choices"][0]["message"]["content"].strip()
            return jsonify({"response": reply})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return jsonify({"status": "ignored"})

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
