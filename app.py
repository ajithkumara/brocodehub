from flask import Flask, request, send_file, jsonify, Response
from gtts import gTTS
import io

app = Flask(__name__)

@app.route("/tts")
def tts():
    text = request.args.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Generate MP3 in memory
        mp3_bytes = io.BytesIO()
        tts = gTTS(text=text, lang="en")
        tts.write_to_fp(mp3_bytes)
        mp3_bytes.seek(0)

        # Build streaming-friendly response
        response = Response(mp3_bytes.read(),
                            mimetype="audio/mpeg")
        response.headers["Content-Type"] = "audio/mpeg"
        response.headers["Accept-Ranges"] = "bytes"

        return response

    except Exception as e:
        print("TTS ERROR:", e)
        return jsonify({"error": str(e)}), 500
