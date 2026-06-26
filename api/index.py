from http.server import BaseHTTPRequestHandler
import json
import requests
import uuid

VOICE = "id-ID-ArdiNeural"

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

        # EDGE TTS via public endpoint (FREE workaround)
        url = "https://api.streamelements.com/kappa/v2/speech"

        payload = {
            "voice": VOICE,
            "text": text
        }

        r = requests.get(
            "https://text-to-speech-api.vercel.app/api/tts",
            params={"text": text, "voice": "id-ID"},
        )

        self.send_response(200)
        self.send_header("Content-Type", "audio/mpeg")
        self.end_headers()
        self.wfile.write(r.content)
