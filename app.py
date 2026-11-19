import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '')
    student = data.get('student', '')
    email = data.get('email', '')

    print(f"Příchozí dotaz od: {student}, email: {email}, zpráva: {message}", flush=True)

    try:
        prompt = (
            "Jsi milý a profesionální asistent zákaznické podpory e-shopu. "
            "Odpovídej stručně, věcně a česky. "
            f"Dotaz zákazníka zní: {message}"
        )

        # Použití rychlého modelu gemini-3.8-flash-lite
        response = client.models.generate_content(
            model="gemini-3.8-flash-lite",
            contents=prompt,
        )
        
        reply_text = response.text

    except Exception as e:
        print(f"Chyba při komunikaci s Gemini: {e}", flush=True)
        reply_text = "Omlouváme se, AI asistent je momentálně přetížený, zkuste to prosím za chvilku."

    return jsonify({'reply': reply_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
