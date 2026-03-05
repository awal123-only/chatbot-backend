from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

# Ambil dari environment variable, fallback ke string langsung untuk debug
api_key = os.environ.get("GROQ_API_KEY", "").strip()
client = Groq(api_key=api_key)

riwayat = []

@app.route("/")
def index():
    # Tampilkan 10 karakter pertama API key untuk debug
    key_preview = api_key[:10] + "..." if api_key else "KOSONG!"
    return f"Chatbot API aktif! 🤖 | Key loaded: {key_preview}"

@app.route("/chat", methods=["POST"])
def chat():
    global riwayat
    data = request.json
    pesan = data.get("pesan", "")

    if not pesan:
        return jsonify({"balasan": "Pesan kosong!"}), 400

    riwayat.append({"role": "user", "content": pesan})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Kamu adalah asisten AI milik Awal Marudut Gultom, seorang Network Engineer dan Python Developer. Jawab pertanyaan tentang Awal atau pertanyaan umum dengan ramah dan singkat."},
                *riwayat
            ],
            max_tokens=1024
        )
        balasan = response.choices[0].message.content
        riwayat.append({"role": "assistant", "content": balasan})
        return jsonify({"balasan": balasan})
    except Exception as e:
        return jsonify({"balasan": f"Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port) 
