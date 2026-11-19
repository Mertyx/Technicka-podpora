import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)

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

    try:
        # Zjistí všechny dostupné modely pro váš API klíč, které umí odpovídat na text
        available_models = []
        for m in client.models.list():
            if "generateContent" in (m.supported_actions or []) and "gemini" in m.name:
                # Upřednostníme flash modely (jsou nejrychlejší)
                if "flash" in m.name:
                    available_models.insert(0, m.name)
                else:
                    available_models.append(m.name)

        print(f"Nalezené modely: {available_models}", flush=True)

        # Postupně zkusí dostupné modely, dokud některý neodpoví
        for model_name in available_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                print(f"Úspěšně odpověděl model: {model_name}", flush=True)
                return jsonify({'reply': response.text})
            except Exception as e:
                print(f"Model {model_name} selhal: {e}", flush=True)

    except Exception as e:
        print(f"Chyba při načítání modelů: {e}", flush=True)

    return jsonify({'reply': "Omlouváme se, všechny AI modely jsou momentálně vytížené, zkuste to prosím za minutku."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
