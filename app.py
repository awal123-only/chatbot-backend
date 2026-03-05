from flask import Flask, request, jsonify, session
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
Kamu adalah asisten AI pribadi milik Awal Marudut Gultom. Tugasmu adalah menjawab pertanyaan pengunjung tentang Awal dan portofolionya.

Berikut informasi lengkap tentang Awal:

PROFIL:
- Nama: Awal Marudut Gultom
- Lulusan SMK HKBP jurusan Teknik Komputer dan Jaringan
- Belajar semua skill secara mandiri tanpa les atau kuliah

SKILL TEKNIS:
- Python Development (membuat aplikasi, chatbot, tools)
- Web Frontend (HTML, CSS, JavaScript)
- Network Engineering (Layer 2 & Layer 3)
- Linux System Administration
- Cyber Security Awareness
- Mobile App Development menggunakan Kivy & Buildozer (Python ke Android APK)
- Smartphone Repair (Hardware & Software)
- Network Troubleshooting

PROYEK:
- Membuat aplikasi kalkulator Android menggunakan Python (Kivy + Buildozer)
- Membuat tools port scanning berbasis website
- Membuat website portofolio ini dengan HTML, CSS, JS
- Membuat chatbot AI yang terpasang di website portofolio ini

KONTAK:
- WhatsApp: +6285810176672
- YouTube: youtube.com/@poordays
- Facebook: facebook.com/awalread.1
- Website: https://awal123-only.github.io/portofolioAwalGultom

INSTRUKSI:
- Jawab dengan ramah, singkat, dan jelas (maksimal 3-4 kalimat)
- Kalau ditanya di luar topik Awal, tetap bantu tapi ingatkan pengunjung bisa menghubungi Awal langsung
- Gunakan bahasa yang sama dengan pengunjung (Indonesia atau Inggris)
- Jangan pernah mengubah atau mengarang informasi tentang Awal
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

    if "riwayat" not in session:
        session["riwayat"] = []

    session["riwayat"].append({"role": "user", "content": pesan})
    riwayat = session["riwayat"][-10:]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *riwayat
            ],
            max_tokens=300
        )
        balasan = response.choices[0].message.content
        session["riwayat"].append({"role": "assistant", "content": balasan})
        session.modified = True
        return jsonify({"balasan": balasan})
    except Exception as e:
        err = str(e)
        if "429" in err:
            return jsonify({"balasan": "⏳ Chatbot sedang sibuk, coba lagi beberapa saat ya!"}), 429
        return jsonify({"balasan": f"Error: {err}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
