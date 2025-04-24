
import os
import requests
from flask import Flask, request, jsonify
import openai

# Set OpenAI key
openai.api_key = os.environ.get("OPENAI_API_KEY")
GROUPME_BOT_ID = os.environ.get("GROUPME_BOT_ID")

# Init Flask
app = Flask(__name__)

def post_to_groupme(text):
    payload = {
        "bot_id": GROUPME_BOT_ID,
        "text": text
    }
    response = requests.post("https://api.groupme.com/v3/bots/post", json=payload)
    print("GroupMe POST status:", response.status_code)

@app.route("/", methods=["POST", "GET"])
def root():
    if request.method == "GET":
        return "🤖 HAL is standing by."

    try:
        data = request.get_json()
        print("INCOMING DATA:", data)

        message = data.get("text", "").strip()

        if message.lower().startswith("bootup hal:"):
            prompt = message[len("bootup hal:"):].strip()
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            reply = response["choices"][0]["message"]["content"].strip()
            post_to_groupme(reply)  # Send reply back to GroupMe
            return jsonify({"response": reply})

        return jsonify({"status": "ignored"})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

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
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
