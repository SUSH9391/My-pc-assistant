import asyncio
import threading
from app.services.stt import listen
from app.services.tts import speak
from app.core.intent_engine import parse_intent
from app.core.executor import execute
from app.logger import get_logger
from app.config import Config
from app.scanner import Scanner

logger = get_logger()

async def process_command(command: str):
    logger.info(f"Command received: {command}")

    intent_data = parse_intent(command)
    intent = intent_data.get("intent")
    entity = intent_data.get("entity")

    result = execute(intent, entity)
    speak(result)

async def main():
    # Init scanner
    scanner = Scanner()
    scanner.index_all()
    speak("Assistant started. Indexing complete with recency/frequency prioritization.")

    while True:
        try:
            command = listen().lower().strip()
            logger.info(f"Heard: '{command}' (wake: {Config.WAKE_WORD in command})")

            if command:
                if Config.WAKE_WORD in command:
                    speak("Yes?")
                    command = command.replace(Config.WAKE_WORD, "").strip()
                else:
                    speak("Listening...")

                await process_command(command)

        except KeyboardInterrupt:
            speak("Goodbye")
            break
        except Exception as e:
            logger.error(f"Loop error: {e}")
            speak("Error occurred.")

if __name__ == "__main__":
    asyncio.run(main())
