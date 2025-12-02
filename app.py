from flask import Flask, request, Response
from gtts import gTTS
import io
from pydub import AudioSegment  # pip install pydub

app = Flask(__name__)

@app.route("/tts")
def tts():
    text = request.args.get("text", "").strip()
    if not text:
        return {"error": "No text provided"}, 400

    try:
        # Step 1: Generate MP3 in memory
        mp3_fp = io.BytesIO()
        tts = gTTS(text=text, lang="en", slow=False)
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        # Step 2: Convert MP3 → WAV (for browser compatibility)
        audio = AudioSegment.from_file(mp3_fp, format="mp3")
        wav_fp = io.BytesIO()
        audio.export(wav_fp, format="wav")
        wav_fp.seek(0)

        # Step 3: Stream WAV response
        def generate():
            wav_fp.seek(0)
            yield from wav_fp

        return Response(
            generate(),
            mimetype="audio/wav",
            headers={
                "Content-Disposition": 'inline; filename="speech.wav"',
                "Accept-Ranges": "bytes",
            }
        )

    except Exception as e:
        print("TTS ERROR:", e)
        return {"error": str(e)}, 500
