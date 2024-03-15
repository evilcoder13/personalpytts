from fastapi import FastAPI, Request, HTTPException
from gtts import gTTS
import pyttsx4
import os
from fastapi.staticfiles import StaticFiles
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/download", StaticFiles(directory="download"), name="download")

@app.post("/tts")
async def tts(request: Request):
    data = await request.json()
    text = data["text"]
    lang = data.get("lang", "vi")
    speed = data.get("speed", 1.0)
    slow = data.get("slow", False)
    model = data.get("model", "pytts")
    filename = data.get("file_name", "output.mp3")
    try:
        if model == "gtts":
            tts = gTTS(text=text, lang=lang, slow=slow)
            tts.save(filename)
        else:
            # Tạo đối tượng TTS
            engine = pyttsx4.init()
            voices = engine.getProperty('voices')
            engine.setProperty('voice', data.get("voice", voices[1].id))

            # engine.setProperty('volume', volume-0.25)
            engine.setProperty('rate', data.get("rate", 50))

            # Đọc văn bản
            #engine.say(text)
            # Lưu file MP3
            engine.save_to_file(text, filename)
            engine.runAndWait()
        if speed == 1.0:
            os.rename(filename, "/app/download/"+filename)
        else:
            from pydub import AudioSegment
            audio = AudioSegment.from_mp3(filename)
            final = audio.speedup(playback_speed=speed)
            final.export("/app/download/"+filename, format="mp3")

        return {"success": True, "file_name": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/voices")
async def voices():
    voices = pyttsx4.init().getProperty('voices')
    return {"voices": [{"name": voice.name, "id": voice.id, "language": voice.languages, "voice":voice} for voice in voices]}
