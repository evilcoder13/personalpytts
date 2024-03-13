from fastapi import FastAPI, Request, HTTPException
from gtts import gTTS
import pyttsx3
import os
app = FastAPI()

@app.post("/tts")
async def tts(request: Request):
    data = await request.json()
    text = data["text"]
    lang = data.get("lang", "vi")
    speed = data.get("speed", 1.0)

    try:
        # Tạo đối tượng TTS
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)

        # Đọc văn bản
        #engine.say(text)

        # Lưu file MP3
        engine.save_to_file(text, "output.mp3")
        engine.runAndWait()
        os.rename("output.mp3", "/app/output1.mp3")

        return {"success": True, "file_name": "output.mp3"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/voices")
async def voices():
    voices = pyttsx3.init().getProperty('voices')
    return {"voices": [{"name": voice.name, "id": voice.id, "language": voice.languages} for voice in voices]}
