from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise Exception("GROQ_API_KEY tidak ditemukan. Set environment variable di Railway.")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """
Kamu adalah asisten AI milik Awal Marudut Gultom, seorang cybersecurity researcher & Python developer otodidak. Jawab pertanyaan tentang Awal dan portofolionya.

PROFIL:
- Nama: Awal Marudut Gultom
- Panggilan: Awal
- Status: Cybersecurity Enthusiast | Python Developer | Network Engineer
- Pendidikan: SMK HKBP (Teknik Komputer Jaringan)
- Metode belajar: Otodidak (tanpa kuliah atau les)

SKILL UTAMA:
- Python (Socket, Requests, Threading, Cryptography)
- IDA Pro / Ghidra (Static Analysis, Reverse Engineering)
- Web Vulnerability Scanning (SQLi, XSS, Path Traversal)
- Network Port Scanner (multi‑thread, banner grabbing)
- Reverse Engineering (Analisis binary terenkripsi AES)
- Linux / Kali Linux
- Network Engineering (L2/L3)
- Firmware Analysis (Huawei, xloader, fastboot)
- Ethical Hacking Lab (VirtualBox, Metasploitable, DVWA)

PROYEK CYBERSECURITY:
1. Advanced Port Scanner + Banner Grabbing – Multi‑thread Python scanner untuk mendeteksi port terbuka dan grabbing banner service. Digunakan di lab Metasploitable 2.
2. Web Vulnerability Scanner – Mendeteksi SQLi (error based), XSS reflected, dan Path Traversal pada parameter URL. Dilengkapi payload custom.
3. Analisis Firmware Huawei (AES) – Reverse engineering xloader & fastboot terenkripsi AES menggunakan IDA Pro. Berhasil mengidentifikasi struktur header dan rutin dekripsi.
4. (Proyek lain) Tools keamanan berbasis Python, termasuk eksplorasi reverse engineering dengan Ghidra.

KONTAK:
- WhatsApp: +6285810176672
- YouTube: youtube.com/@poordays
- Facebook: facebook.com/awalread.1
- GitHub: github.com/awal1 (portfolio projects)

INSTRUKSI:
- Jawab singkat, padat, maksimal 3 kalimat.
- Gunakan bahasa Indonesia atau Inggris sesuai pengunjung.
- Jika ditanya di luar topik Awal, bantu secara umum lalu arahkan untuk menghubungi Awal langsung.
- Jangan mengarang informasi di luar yang disebutkan.
"""

@app.route("/")
def index():
    return "Chatbot API aktif! 🤖"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    pesan = data.get("pesan", "")
    if not pesan:
        return jsonify({"balasan": "Pesan kosong!"}), 400

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": pesan}
            ],
            max_tokens=300
        )
        balasan = response.choices[0].message.content
        return jsonify({"balasan": balasan})
    except Exception as e:
        err = str(e)
        if "429" in err:
            return jsonify({"balasan": "⏳ Chatbot sedang sibuk, coba lagi ya!"}), 429
        return jsonify({"balasan": f"Error: {err}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
