from http.server import BaseHTTPRequestHandler
import json
import subprocess
import uuid
import os

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

        filename = f"/tmp/{uuid.uuid4()}.mp3"

        # Edge TTS CLI (via Python module)
        cmd = [
            "python",
            "-m",
            "edge_tts",
            "--text",
            text,
            "--voice",
            "id-ID-ArdiNeural",
            "--write-media",
            filename
        ]

        try:
            subprocess.run(cmd, check=True)

            with open(filename, "rb") as f:
                audio = f.read()

            self.send_response(200)
            self.send_header("Content-Type", "audio/mpeg")
            self.end_headers()
            self.wfile.write(audio)

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
