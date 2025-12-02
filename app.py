# app.py
from flask import Flask, request, send_file, jsonify
import pyaudio
import wave
from gtts import gTTS
import soundfile as sf
import uuid
import os

app = Flask(__name__)

# Function to generate speech and save it to a WAV file
def text_to_speech(text, filename):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)

    data, samplerate = sf.read(filename)
    sf.write(filename, data, samplerate)

@app.route('/tts', methods=['POST'])
def tts_api():
    data = request.json
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    # Unique filename
    filename = f"audio_{uuid.uuid4().hex}.wav"

    # Generate speech
    text_to_speech(text, filename)

    # Return WAV file
    return send_file(filename, mimetype="audio/wav")
    

@app.route('/')
def home():
    return "TTS Backend is Running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
