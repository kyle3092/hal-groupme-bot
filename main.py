
import os
import openai
from flask import Flask, request

app = Flask(__name__)

client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

GROUPME_BOT_ID = os.environ["GROUPME_BOT_ID"]

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    if "text" in data and data["sender_type"] != "bot":
        message_text = data["text"]

        # Basic trigger check
        if message_text.lower().startswith("bootup hal:"):
            prompt = message_text.split("bootup hal:", 1)[1].strip()

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are HAL, a sassy and funny assistant for a gun range called Top Gun."},
                    {"role": "user", "content": prompt}
                ]
            )

            reply = response.choices[0].message.content.strip()

            # Respond back to GroupMe
            import requests
            requests.post("https://api.groupme.com/v3/bots/post", json={
                "bot_id": GROUPME_BOT_ID,
                "text": reply
            })
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
