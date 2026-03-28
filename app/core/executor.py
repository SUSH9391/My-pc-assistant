import os
from loguru import logger

def execute(intent, entity):
    from app.scanner import Scanner
    indexer = Scanner()
    try:
        if intent == "open_app":
            # Expand ~ to user home
            entity = os.path.expanduser(entity)
            # Try startfile first, then system
            try:
                os.startfile(entity)
            except OSError:
                os.system(f'start "" "{entity}"')            indexer.update_access(entity)
            return f"Opening app: {entity}"

        elif intent == "open_file":
            entity = os.path.expanduser(entity)
            os.startfile(entity)
            indexer.update_access(entity)
            return f"Opening file: {entity}"

        elif intent == "open_daily_tools":
            top_items = indexer.get_top_items(n=5)
            opened = []
            for item in top_items:
                path = os.path.expanduser(item['path'])
                try:
                    os.startfile(path)
                    indexer.update_access(path)
                    opened.append(item['name'])
                except:
                    os.system(f'start "" "{path}"')
                    indexer.update_access(path)
                    opened.append(item['name'])
            return f"Opened top daily tools: {', '.join(opened)}"

        else:
            return f"Command '{intent}' with '{entity}' not recognized yet"

    except Exception as e:
        logger.error(f"Execution failed: {e}")
        return f"Error executing: {e}"

