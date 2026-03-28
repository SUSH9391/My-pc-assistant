import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    APP_NAME = "my-pc-assistant"
    DEBUG = os.getenv("DEBUG", "False") == "True"

    # LLM
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")
    OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")

    # Scanner
    SCAN_PATHS = [
        r"C:\Program Files",
        r"C:\Program Files (x86)",
        r"C:\Users\Lenovo\Desktop",
        r"C:\Users\Lenovo\Start Menu\Programs"
    ]
    EXCLUDE_PATTERNS = [
        r"\\Windows$",
        r"\\System32$",
        r"\\ProgramData$",
        r"\\$Recycle\.Bin$",
        r"node_modules",
        r"\.git",
        r"__pycache__"
    ]
    VOICE_ID = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0"

    # Assistant
    WAKE_WORD = "hey sam"
