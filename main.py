
import os
import requests
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Initialize OpenAI client manually
openai.api_key = os.environ["OPENAI_API_KEY"]

CUSTOM_GPT_ID = "g-681033e9e3ac8191b78f5c7e93bcb3f7"

bot_disabled = False

@app.route("/", methods=["POST"])
def webhook():
    global bot_disabled

    if bot_disabled:
        return jsonify(status="bot disabled due to previous critical error"), 503

    data = request.get_json()
    message_text = data.get("text", "")
    groupme_bot_id = os.environ["GROUPME_BOT_ID"]

    try:
        response = openai.ChatCompletion.create(
            model=CUSTOM_GPT_ID,
            messages=[
                {"role": "user", "content": message_text}
            ],
            headers={
                "OpenAI-Beta": "assistants=v2"
            }
        )
        reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"OpenAI API Error: {e}", flush=True)
        bot_disabled = True  # Immediately disable bot on ANY error
        reply = "Critical error detected. HAL is shutting down to prevent spam."

    # Only send a response if not yet disabled, or if sending the shutdown notice
    if not bot_disabled or "shutting down" in reply:
        requests.post("https://api.groupme.com/v3/bots/post", json={
            "bot_id": groupme_bot_id,
            "text": reply
        })

    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
