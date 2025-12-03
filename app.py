# app.py
import os
from flask import Flask, request, Response, send_from_directory
import pyttsx3
import tempfile

app = Flask(__name__)

# Initialize engine once
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        _engine = pyttsx3.init()
        # Use espeak voices (Render uses Linux → espeak)
        # List voices: [v.id for v in _engine.getProperty('voices')]
        # 'en-us' (default), 'en+f1' (female), 'en+m1' (male)
        _engine.setProperty('voice', 'en+m1')  # 👈 MALE voice!
        _engine.setProperty('rate', 150)
    return _engine

@app.route("/")
def home():
    return send_from_directory(".", "tts.html")

@app.route("/tts")
def tts():
    text = request.args.get("text", "").strip()
    if not text:
        return {"error": "No text"}, 400

    # Safety: limit length
    text = text[:150]

    try:
        engine = get_engine()
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name

        engine.save_to_file(text, tmp_path)
        engine.runAndWait()

        with open(tmp_path, 'rb') as f:
            data = f.read()
        os.unlink(tmp_path)

        if len(data) < 100:
            return {"error": "Generated empty audio"}, 500

        return Response(
            data,
            mimetype="audio/wav",
            headers={
                "Content-Length": str(len(data)),
                "Accept-Ranges": "bytes",
            }
        )

    except Exception as e:
        import traceback
        print("❌ TTS ERROR:")
        traceback.print_exc()
        return {"error": str(e)}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)