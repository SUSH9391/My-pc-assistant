import pyttsx3
from loguru import logger

engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    if text:
        logger.info(f"Speaking: {text}")
        engine.say(text)
        engine.runAndWait()
