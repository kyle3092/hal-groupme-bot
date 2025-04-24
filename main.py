import openai
import requests
from flask import Flask, request
import os

app = Flask(__name__)

GROUPME_BOT_ID = os.environ['GROUPME_BOT_ID']
OPENAI_API_KEY = os.environ['OPENAI_API_KEY']

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data:
        return "No data", 400

    message = data.get("text", "")
    sender = data.get("name", "Someone")

    if message.lower().startswith("bootup hal:"):
        prompt = message[len("bootup hal:"):].strip()

        openai.api_key = OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are HAL, a smart, sassy, and knowledgeable AI assistant for Top Gun Range staff. Be funny but always helpful."},
                {"role": "user", "content": prompt}
            ]
        )

        reply = response['choices'][0]['message']['content']
        send_to_groupme(f"{sender}, HAL says: {reply}")

    return "OK", 200

def send_to_groupme(message):
    url = "https://api.groupme.com/v3/bots/post"
    payload = {"bot_id": GROUPME_BOT_ID, "text": message}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
