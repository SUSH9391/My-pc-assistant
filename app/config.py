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

    # Assistant
    WAKE_WORD = "hey sam"
