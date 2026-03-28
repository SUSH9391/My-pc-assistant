from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, level="INFO")
logger.add("assistant.log", rotation="1 MB")

def get_logger():
    return logger
