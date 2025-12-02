from flask import Flask, request, send_file, jsonify
from flask_cors import CORS # Import CORS to allow browser requests
from gtts import gTTS
import io

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route("/tts")
def tts():
    text = request.args.get("text", "")
    
    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # Generate MP3 in memory
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang="en")
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        # distinct advantage: send_file handles headers automatically
        return send_file(
            mp3_fp,
            mimetype="audio/mpeg",
            as_attachment=False,
            download_name="tts.mp3"
        )

    except Exception as e:
        print("TTS ERROR:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
