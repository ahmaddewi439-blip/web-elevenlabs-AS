from http.server import BaseHTTPRequestHandler
import json
import requests
from urllib.parse import quote


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(405)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({
            "error": "Gunakan POST untuk generate audio"
        }).encode())

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body)

            text = data.get("text", "").strip()

            if not text:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "Text kosong"
                }).encode())
                return

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

            response = requests.get(url, params=params, headers=headers, timeout=20)

            if response.status_code != 200:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "error": "Gagal generate audio"
                }).encode())
                return

            self.send_response(200)
            self.send_header("Content-Type", "audio/mpeg")
            self.end_headers()
            self.wfile.write(response.content)

        except Exception as e:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": str(e)
            }).encode())
