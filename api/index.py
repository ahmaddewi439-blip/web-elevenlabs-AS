from http.server import BaseHTTPRequestHandler
import json
import requests
import os

# 1. API KEY ELEVENLABS ANDA
ELEVENLABS_API_KEY = "1d77699397af97ef254cdec00614f02d4ccc9afe002ad1fc5edd709188a02b79"

class handler(BaseHTTPRequestHandler):

    # ----------------------------------------------------
    # FUNGSI BARU: Menangani web saat dibuka (Metode GET)
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # Otomatis mencari dan menampilkan file index.html Anda
        try:
            path = 'index.html'
            if not os.path.exists(path):
                path = '../index.html' # Jalur cadangan
                
            with open(path, 'rb') as file:
                self.wfile.write(file.read())
        except Exception as e:
            self.wfile.write(b"Server Python menyala, tapi file index.html tidak ditemukan di Vercel.")
    # ----------------------------------------------------

    # FUNGSI LAMA: Menangani pemrosesan suara (Metode POST)
    def do_POST(self):
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
        voice_id = data.get("voice_id", "21m00Tcm4TlvDq8ikWAM")

        if not text:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Text kosong")
            return

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }

        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2", 
            "voice_settings": {
                "stability": 0.5,        
                "similarity_boost": 0.75 
            }
        }

        try:
            r = requests.post(url, json=payload, headers=headers)

            if r.status_code == 200:
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.end_headers()
                self.wfile.write(r.content)
            else:
                self.send_response(r.status_code)
                self.end_headers()
                error_msg = f"ElevenLabs Error: {r.text}".encode('utf-8')
                self.wfile.write(error_msg)
                
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Server Error: {str(e)}".encode('utf-8'))
