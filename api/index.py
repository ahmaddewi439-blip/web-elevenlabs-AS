from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

VOICE_ID = "1ijzBXcD3AIVH8RGMcQd"
API_KEY = "sk_0a1305f6f3a9780dceb85f2441b0af1805b8ef00d7d5cad6"

@app.route("/api/generate-audio", methods=["POST"])
def generate_audio():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Text kosong"}), 400

    text = data["text"]

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }

    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    r = requests.post(url, json=payload, headers=headers)

    if r.status_code != 200:
        return jsonify({
            "error": "ElevenLabs error",
            "detail": r.text
        }), 500

    return Response(r.content, mimetype="audio/mpeg")


# 🔥 INI YANG WAJIB UNTUK VERCEL
app = app
