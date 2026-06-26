from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel
ELEVANLABS_API_KEY = "sk_0a1305f6f3a9780dceb85f2441b0af1805b8ef00d7d5cad6"

@app.route('/api/generate-audio', methods=['POST'])
def generate_audio():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "Text kosong"}), 400

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVANLABS_API_KEY
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        return jsonify({
            "error": "ElevenLabs error",
            "detail": response.text
        }), 500

    return Response(response.content, mimetype="audio/mpeg")
