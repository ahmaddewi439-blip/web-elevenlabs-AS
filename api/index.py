from http.server import BaseHTTPRequestHandler
import json
import requests
import os

# MASUKKAN TOKEN HUGGING FACE ANDA DI BAWAH INI (Yang berawalan hf_...)
HF_TOKEN = "MASUKKAN_TOKEN_HF_ANDA_DISINI"

# File suara Anda sudah terdeteksi di folder
FILE_SUARA = "lv_0_20260707092058.mp3"

class handler(BaseHTTPRequestHandler):
    
    # Fungsi agar web HTML tetap bisa terbuka
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        try:
            path = 'index.html'
            if not os.path.exists(path):
                path = '../index.html'
            with open(path, 'rb') as file:
                self.wfile.write(file.read())
        except Exception as e:
            self.wfile.write(b"File HTML tidak ditemukan.")

    # Fungsi untuk memproses teks menjadi suara
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

        if not text:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Text kosong")
            return

        # URL API Hugging Face (Kita tes dengan model TTS dasar dulu)
        API_URL = "https://api-inference.huggingface.co/models/facebook/mms-tts-ind"
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        payload = {"inputs": text}

        try:
            # Vercel akan memutus paksa jika lebih dari 10 detik, jadi kita set timeout 9 detik
            response = requests.post(API_URL, headers=headers, json=payload, timeout=9)

            if response.status_code == 200:
                self.send_response(200)
                # Format dari model HF ini biasanya FLAC atau WAV
                self.send_header("Content-Type", "audio/flac")
                self.end_headers()
                self.wfile.write(response.content)
            else:
                self.send_response(response.status_code)
                self.end_headers()
                error_msg = f"Hugging Face API Error: {response.text}".encode('utf-8')
                self.wfile.write(error_msg)
                
        except requests.exceptions.Timeout:
            self.send_response(504)
            self.end_headers()
            self.wfile.write(b"Timeout: Vercel memutus koneksi karena AI butuh waktu lebih dari 10 detik.")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Server Error: {str(e)}".encode('utf-8'))
