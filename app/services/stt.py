import speech_recognition as sr
from loguru import logger

def listen():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            logger.info("Listening...")
            audio = r.listen(source, timeout=5)
        text = r.recognize_google(audio).lower()
        logger.info(f"Recognized: {text}")
        return text
    except sr.UnknownValueError:
        logger.warning("Could not understand audio")
        return ""
    except sr.RequestError as e:
        logger.error(f"Speech recognition error: {e}")
        return ""
    except Exception as e:
        logger.error(f"STT error: {e}")
        return ""
