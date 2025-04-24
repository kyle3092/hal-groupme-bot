import os
import requests
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    message_text = data.get("text", "")
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are HAL, an AI assistant for Top Gun Range."},
            {"role": "user", "content": message_text}
        ]
    )

    reply = response.choices[0].message.content
    groupme_bot_id = os.environ["GROUPME_BOT_ID"]

    requests.post("https://api.groupme.com/v3/bots/post", json={
        "bot_id": groupme_bot_id,
        "text": reply
    })

    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
