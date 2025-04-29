
import os
import requests
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Assistant ID from platform.openai.com
CUSTOM_GPT_ID = "asst_q47OlATyb2246GuEBi1iXPYU"

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
        client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model=CUSTOM_GPT_ID,
            messages=[
                {"role": "user", "content": message_text}
            ],
            extra_headers={
                "OpenAI-Beta": "assistants=v2"
            }
        )
        reply = response.choices[0].message.content
    except Exception as e:
        print("❌ OpenAI API Error:", flush=True)
        print(e, flush=True)
        bot_disabled = True
        reply = "Critical error detected. HAL is shutting down to prevent spam."

    if not bot_disabled or "shutting down" in reply:
        requests.post("https://api.groupme.com/v3/bots/post", json={
            "bot_id": groupme_bot_id,
            "text": reply
        })

    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
