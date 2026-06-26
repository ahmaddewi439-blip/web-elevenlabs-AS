from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

VOICE_ID = "21m00Tcm4TlvDq8ikWAM"
ELEVANLABS_API_KEY = "sk_0a1305f6f3a9780dceb85f2441b0af1805b8ef00d7d5cad6"

@app.route('/api/generate-audio', methods=['POST'])
def generate_audio():
    data = request.json
    teks = data.get("text", "")

    if not teks:
        return jsonify({"error": "Teks tidak boleh kosong"}), 400

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVANLABS_API_KEY
    }

    payload = {
        "text": teks,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    return response.content, 200, {
        "Content-Type": "audio/mpeg"
    }
