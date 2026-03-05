from flask import Flask, request, jsonify, session
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app, supports_credentials=True)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = "Kamu adalah asisten AI milik Awal Marudut Gultom, seorang Network Engineer dan Python Developer. Jawab pertanyaan tentang Awal atau pertanyaan umum dengan ramah dan singkat. Maksimal 3 kalimat per jawaban agar hemat."

@app.route("/")
def index():
    return "Chatbot API aktif! 🤖"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    pesan = data.get("pesan", "")

    if not pesan:
        return jsonify({"balasan": "Pesan kosong!"}), 400

    # Riwayat per sesi (per user)
    if "riwayat" not in session:
        session["riwayat"] = []

    session["riwayat"].append({"role": "user", "content": pesan})

    # Batasi riwayat max 10 pesan agar hemat token
    riwayat = session["riwayat"][-10:]

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # Model ringan, hemat token
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                *riwayat
            ],
            max_tokens=300  # Batasi panjang jawaban
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
