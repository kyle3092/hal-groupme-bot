
import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

openai.api_key = os.environ["OPENAI_API_KEY"]

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    user_message = data.get("text", "")

    if user_message.lower().startswith("bootup hal:"):
        prompt = user_message[len("bootup hal:"):].strip()

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are HAL, an AI assistant for a shooting range."},
                {"role": "user", "content": prompt},
            ]
        )

        reply = response.choices[0].message.content.strip()
        return jsonify({"text": reply})

    return jsonify({"text": "Command not recognized."})

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
