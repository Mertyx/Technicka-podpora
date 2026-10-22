from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Povolí komunikaci s webovou stránkou

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json() or {}
    message = data.get('message', '')
    student = data.get('student', '')
    email = data.get('email', '')

    print(f"Příchozí dotaz od: {student}, email: {email}, zpráva: {message}")

    msg_lower = message.lower()
    if 'platba' in msg_lower or 'faktura' in msg_lower:
        reply_text = "Platbu můžete provést kartou nebo bankovním převodem."
    elif 'vraceni' in msg_lower or 'vrátit' in msg_lower:
        reply_text = "Zboží můžete vrátit do 14 dnů bez udání důvodu."
    else:
        reply_text = f"Ahoj {student}, tvůj dotaz ('{message}') byl úspěšně zpracován na tvém Python backendu!"

    return jsonify({'reply': reply_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
