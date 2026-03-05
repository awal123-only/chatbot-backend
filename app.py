from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)  # Izinkan akses dari portofolio GitHub Pages

# Ambil API key dari environment variable Railway
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-lite",
    system_instruction="Kamu adalah asisten AI milik Awal Marudut Gultom. Jawab pertanyaan tentang Awal atau pertanyaan umum dengan ramah dan singkat."
)

# Simpan riwayat per sesi (sederhana)
riwayat = []

@app.route("/")
def index():
    return "Chatbot API aktif! 🤖"

@app.route("/chat", methods=["POST"])
def chat():
    global riwayat
    data = request.json
    pesan = data.get("pesan", "")

    if not pesan:
        return jsonify({"balasan": "Pesan kosong!"}), 400

    riwayat.append({"role": "user", "content": pesan})

    try:
        chat_session = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]} for m in riwayat[:-1]
        ])
        response = chat_session.send_message(pesan)
        balasan = response.text
        riwayat.append({"role": "model", "content": balasan})
        return jsonify({"balasan": balasan})
    except Exception as e:
        return jsonify({"balasan": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
