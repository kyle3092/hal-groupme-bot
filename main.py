
import os
import openai
from flask import Flask, request, jsonify

app = Flask(__name__)

openai.api_key = os.environ["OPENAI_API_KEY"]

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()
    prompt = data["text"]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are HAL, a helpful and sassy assistant at Top Gun Range."},
                {"role": "user", "content": prompt}
            ]
        )
        return jsonify({"text": response.choices[0].message["content"]})
    except Exception as e:
        return jsonify({"text": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
