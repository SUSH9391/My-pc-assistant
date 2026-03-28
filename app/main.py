import asyncio
from app.services.stt import listen
from app.services.tts import speak
from app.core.intent_engine import parse_intent
from app.core.executor import execute
from app.logger import get_logger
from app.config import Config

logger = get_logger()

async def process_command(command: str):
    logger.info(f"Command received: {command}")

    intent_data = parse_intent(command)
    intent = intent_data.get("intent")
    entity = intent_data.get("entity")

    result = execute(intent, entity)
    speak(result)

async def main():
    speak("Assistant started")

    while True:
        try:
            command = listen().lower().strip()
            logger.info(f"Heard command: '{command}' (wake match: '{Config.WAKE_WORD}' in it: {Config.WAKE_WORD in command})")

            if command:
                if Config.WAKE_WORD in command:
                    speak("Yes sir")
                    command = command.replace(Config.WAKE_WORD, "").strip()
                else:
                    speak("Processing command")

                await process_command(command)

        except KeyboardInterrupt:
            speak("Goodbye")
            break
        except Exception as e:
            logger.error(f"Error in loop: {e}")

if __name__ == "__main__":
    asyncio.run(main())
