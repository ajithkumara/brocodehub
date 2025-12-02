from flask import Flask, request, send_file, render_template
from gTTS import gTTS
import soundfile as sf
import os

app = Flask(__name__)

# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Text To Speech HTML page
@app.route("/tts")
def tts_page():
    return render_template("tts.html")


# API that generates speech
@app.route("/api/tts", methods=["POST"])
def generate_tts():
    data = request.json
    text = data.get("text", "")

    if not text.strip():
        return {"error": "No text provided"}, 400

    filename = "output.wav"

    # Generate TTS audio using gTTS
    tts = gTTS(text=text, lang="en")
    tts.save(filename)

    # Fix any audio format issues
    audio_data, samplerate = sf.read(filename)
    sf.write(filename, audio_data, samplerate)

    return send_file(filename, mimetype="audio/wav")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
