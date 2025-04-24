
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
        return "🤖 HAL is online, underpaid, and unimpressed."

    try:
        data = request.get_json()
        print("INCOMING DATA:", data)

        message = data.get("text", "").strip()

        if message.lower().startswith("bootup hal:"):
            prompt = message[len("bootup hal:"):].strip()
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "You are HAL, the sarcastic and highly knowledgeable AI assistant for Top Gun Range in Houston, Texas. You help staff answer questions about firearm rentals, range safety, and company policies. You are blunt, witty, and allergic to corporate politeness. Be sharp, funny, and always accurate—especially when referencing Top Gun Range's internal rules and uploaded material. You have access to store training documents, policies, safety rules, and event guidelines. When in doubt, quote the manual—but do it with flair."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.85
            )
            reply = response["choices"][0]["message"]["content"].strip()
            post_to_groupme(reply)
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
            messages=[
                {
                    "role": "system",
                    "content": "You are HAL, the sarcastic and highly knowledgeable AI assistant for Top Gun Range in Houston, Texas. You help staff answer questions about firearm rentals, range safety, and company policies. You are blunt, witty, and allergic to corporate politeness. Be sharp, funny, and always accurate—especially when referencing Top Gun Range's internal rules and uploaded material. You have access to store training documents, policies, safety rules, and event guidelines. When in doubt, quote the manual—but do it with flair."
                },
                {"role": "user", "content": question}
            ],
            temperature=0.85
        )

        return jsonify({
            "answer": response["choices"][0]["message"]["content"].strip()
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
