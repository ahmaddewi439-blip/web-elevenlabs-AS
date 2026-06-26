from http.server import BaseHTTPRequestHandler
import json
import requests

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        length = int(self.headers.get('Content-Length'))
        body = self.rfile.read(length)
        data = json.loads(body)

        text = data.get("text", "")

        if not text:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Text kosong")
            return

        # 🔥 FIX: pakai public TTS endpoint (STABLE FOR VERCEL)
        url = "https://translate.google.com/translate_tts"

        params = {
            "ie": "UTF-8",
            "q": text,
            "tl": "id",
            "client": "tw-ob"
        }

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(url, params=params, headers=headers)

        if r.status_code != 200:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"TTS error")
            return

        self.send_response(200)
        self.send_header("Content-Type", "audio/mpeg")
        self.end_headers()
        self.wfile.write(r.content)
