import os

from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    resume = data.get("resume", "").strip()

    if not resume:
        return jsonify({
            "error": "Please paste your resume first."
        }), 400

    prompt = f"""
You are a funny but genuinely useful AI resume reviewer.

Analyze this resume:

{resume}

Give:
1. A short overall roast.
2. Three things that are weak or boring.
3. Three things that are actually good.
4. Three specific improvements.
5. A funny final verdict.

Be playful, but don't be cruel. Keep the advice useful.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return jsonify({
            "feedback": response.text
        })

    except Exception as e:
        return jsonify({
            "error": f"AI error: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)