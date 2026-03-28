import os
from loguru import logger

def execute(intent, entity):
    try:
        if intent == "open_app":
            # Expand ~ to user home
            entity = os.path.expanduser(entity)
            # Try startfile first, then system
            try:
                os.startfile(entity)
            except:
                os.system(f'start "" "{entity}"')
            return f"Opening app: {entity}"

        elif intent == "open_file":
            entity = os.path.expanduser(entity)
            os.startfile(entity)
            return f"Opening file: {entity}"

        else:
            return f"Command '{intent}' with '{entity}' not recognized yet"

    except Exception as e:
        logger.error(f"Execution failed: {e}")
        return f"Error executing: {e}"

