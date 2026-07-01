from http.server import BaseHTTPRequestHandler
import json
import requests

# 1. MASUKKAN API KEY ELEVENLABS ANDA DI DALAM TANDA KUTIP DI BAWAH INI
ELEVENLABS_API_KEY = "1d77699397af97ef254cdec00614f02d4ccc9afe002ad1fc5edd709188a02b79"

# 2. VOICE ID (Ini adalah ID untuk suara "Rachel", suara wanita natural)
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        # Membaca data yang dikirim dari web (frontend)
        length_header = self.headers.get('Content-Length')
        if not length_header:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Content-Length tidak ditemukan")
            return
            
        length = int(length_header)
        body = self.rfile.read(length)
        data = json.loads(body)

        text = data.get("text", "")

        if not text:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Text kosong")
            return

        # 🔥 MENGGUNAKAN API ELEVENLABS
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

        # Headers khusus untuk ElevenLabs
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }

        # Pengaturan suara agar mirip manusia asli
        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2", # Model ini sangat bagus untuk bahasa Indonesia
            "voice_settings": {
                "stability": 0.5,        # 0.5 membuat intonasi lebih dinamis dan tidak kaku
                "similarity_boost": 0.75 # Menjaga kejelasan artikulasi
            }
        }

        try:
            # Mengirimkan teks ke server ElevenLabs
            r = requests.post(url, json=payload, headers=headers)

            if r.status_code == 200:
                # Jika sukses, kembalikan file audio MP3 ke web
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.end_headers()
                self.wfile.write(r.content)
            else:
                # Jika gagal (misal API key salah atau kuota habis)
                self.send_response(r.status_code)
                self.end_headers()
                error_msg = f"ElevenLabs Error: {r.text}".encode('utf-8')
                self.wfile.write(error_msg)
                
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Server Error: {str(e)}".encode('utf-8'))
