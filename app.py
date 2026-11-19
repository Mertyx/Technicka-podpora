import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)

# Nastavení timeoutu na 15 sekund (15000 ms), aby server nikdy nezamrzl
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=15000)
)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '')
    student = data.get('student', '')
    email = data.get('email', '')

    print(f"Příchozí dotaz od: {student}, email: {email}, zpráva: {message}", flush=True)

    prompt = (
        "Jsi milý a profesionální asistent zákaznické podpory e-shopu. "
        "Odpovídej stručně, věcně a česky. "
        f"Dotaz zákazníka zní: {message}"
    )

    # Zkusí primární model, a pokud je přetížený, zkusí záložní
    models_to_try = ["gemini-3.8-flash", "gemini-3.8-pro"]
    
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            return jsonify({'reply': response.text})
        except Exception as e:
            print(f"Model {model_name} selhal: {e}", flush=True)

    return jsonify({'reply': "Omlouváme se, AI asistent je momentálně přetížený, zkuste to prosím za chvilku."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
