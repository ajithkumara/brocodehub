from flask import Flask, request, send_file, jsonify
from gtts import gTTS
import io

app = Flask(__name__)

@app.route("/tts")
def tts():
    text = request.args.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Generate MP3 directly in memory
        mp3_bytes = io.BytesIO()
        tts = gTTS(text=text, lang="en")
        tts.write_to_fp(mp3_bytes)
        mp3_bytes.seek(0)

        return send_file(
            mp3_bytes,
            mimetype="audio/mpeg",
            as_attachment=False,
            download_name="speech.mp3"
        )

    except Exception as e:
        print("TTS ERROR:", e)
        return jsonify({"error": str(e)}), 500
