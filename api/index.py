from flask import Flask, request, Response
import requests as req

app = Flask(__name__)

# Ganti dengan API Key ElevenLabs Anda yang tadi sudah dibuat
ELEVENLABS_API_KEY = "sk_0a1305f6f3a9780dceb85f2441b0af1805b8ef00d7d5cad6"
VOICE_ID = "21m00Tcm4TlvDq8ikWAM" # Ini ID untuk suara "Rachel"

@app.route('/api/generate-audio', methods=['POST'])
def generate_audio():
    data = request.json
    teks = data.get("text", "")

    if not teks:
        return {"error": "Teks tidak boleh kosong"}, 400

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    
    payload = {
        "text": teks,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    # Mengirim request ke ElevenLabs
    response = req.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return Response(response.content, mimetype="audio/mpeg")
    else:
        return {"error": "Gagal menghasilkan suara"}, 500

# Baris ini wajib untuk Vercel
if __name__ == '__main__':
    app.run(debug=True)