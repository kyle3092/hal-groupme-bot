
import os
import requests
from flask import Flask, request, jsonify
import openai
import time
import random

app = Flask(__name__)

# Initialize OpenAI client manually
openai.api_key = os.environ["OPENAI_API_KEY"]

CUSTOM_GPT_ID = "g-681033e9e3ac8191b78f5c7e93bcb3f7"  # <-- Updated with your Custom GPT ID

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message_text = data.get("text", "")
    groupme_bot_id = os.environ["GROUPME_BOT_ID"]

    max_retries = 1
    for attempt in range(max_retries + 1):
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
            break
        except Exception as e:
            if attempt < max_retries:
                wait_time = random.uniform(0.5, 1.5)  # random wait between 0.5 and 1.5 seconds
                time.sleep(wait_time)
                continue
            else:
                reply = "I'm having trouble reaching the server right now. Please try again later."

    requests.post("https://api.groupme.com/v3/bots/post", json={
        "bot_id": groupme_bot_id,
        "text": reply
    })

    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
