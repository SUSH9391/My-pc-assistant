from loguru import logger
import os

def ensure_data_dir():
    from app.config import Config
    os.makedirs(Config.DATA_DIR, exist_ok=True)
    logger.info(f"Data dir ready: {Config.DATA_DIR}")

def is_exe(path):
    """Check if path is executable"""
    return os.path.isfile(path) and os.access(path, os.X_OK)
