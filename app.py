from flask import Flask, request, Response, send_from_directory
from gtts import gTTS
import io
import os

app = Flask(__name__)

# Route 1: Serve the main page
@app.route("/")
def home():
    return send_from_directory(".", "tts.html")  # reads tts.html from current dir

# Route 2: TTS API
@app.route("/tts")
def tts():
    text = request.args.get("text", "").strip()
    if not text:
        return {"error": "No text provided"}, 400

    try:
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang="en", slow=False)
        tts.write_to_fp(mp3_fp)
        mp3_data = mp3_fp.getvalue()

        return Response(
            mp3_data,
            mimetype="audio/mpeg",
            headers={
                "Content-Length": str(len(mp3_data)),
                "Accept-Ranges": "bytes",
            }
        )
    except Exception as e:
        print("❌ TTS ERROR:", e)
        return {"error": str(e)}, 500

if __name__ == "__main__":
    # Ensure tts.html is in the same folder as app.py
    app.run(host="127.0.0.1", port=5000, debug=True)