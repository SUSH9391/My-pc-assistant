import pyttsx3
from loguru import logger
from app.config import Config

engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Set female voice for Windows (Zira)
voices = engine.getProperty('voices')
female_voice_id = Config.VOICE_ID
for voice in voices:
    if 'zira' in voice.id.lower() or 'female' in voice.name.lower():
        female_voice_id = voice.id
        break
engine.setProperty('voice', female_voice_id)
logger.info(f"Voice set to: {female_voice_id}")

def speak(text):
    if text:
        logger.info(f"Speaking: {text}")
        engine.say(text)
        engine.runAndWait()

if __name__ == "__main__":
    speak("Voice test: Female voice configured for my-pc-assistant.")

