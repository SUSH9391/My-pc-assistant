import os
from loguru import logger

def execute(intent, entity):
    try:
        if intent == "open_app":
            os.system(f'"{entity}"')
            return f"Opening {entity}"

        elif intent == "open_file":
            os.startfile(entity)
            return f"Opening file {entity}"

        else:
            return f"Command '{intent}' with '{entity}' not recognized yet"

    except Exception as e:
        logger.error(f"Execution failed: {e}")
        return f"Error executing command: {e}"
