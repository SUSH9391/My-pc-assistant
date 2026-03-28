from loguru import logger
import ollama
import json
import os
import re

def parse_intent(text: str):
    # Fallback keyword parsing if LLM fails
    text_lower = text.lower()
    if 'daily work tools' in text_lower or 'frequent apps' in text_lower:
        return {"intent": "open_daily_tools", "entity": ""}
    if 'open ' in text_lower:
        if any(app in text_lower for app in ['notepad', 'calc', 'chrome', 'spotify', 'recycle']):
            return {"intent": "open_app", "entity": map_app_name(text)}
        else:
            # Assume file
            entity = text.split('open ', 1)[1].strip()
            return {"intent": "open_file", "entity": entity}
    return {"intent": "unknown", "entity": ""}

def map_app_name(text: str):
    text_lower = text.lower()
    mappings = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'chrome': 'chrome.exe',
        'spotify': 'spotify.exe',
        'recycle bin': 'explorer.exe $Recycle.Bin',
        'documents': os.path.expanduser('~\\Documents')
    }
    for key, value in mappings.items():
        if key in text_lower:
            return value
    return text.split('open ', 1)[1].strip() + '.exe'

def llm_parse(text: str):
    """LLM parsing with Ollama"""
    try:
        user_name = os.getenv('USERNAME', 'User')
        prompt = f"""
        Parse PC command for Windows assistant ({user_name}).
        Examples:
        - "open notepad" → {{"intent": "open_app", "entity": "notepad.exe"}}
        - "open chrome" → {{"intent": "open_app", "entity": "chrome.exe"}} 
        - "open spotify" → {{"intent": "open_app", "entity": "spotify.exe"}}
        - "open recycle bin" → {{"intent": "open_app", "entity": "explorer.exe $Recycle.Bin"}}
        - "open resume" → {{"intent": "open_file", "entity": "~\\Desktop\\resume.pdf"}}
        - "open Documents" → {{"intent": "open_file", "entity": "C:\\\\Users\\\\{user_name}\\\\Documents"}}
        - "open my daily work tools" → {{"intent": "open_daily_tools", "entity": ""}}
        - "open frequent apps" → {{"intent": "open_daily_tools", "entity": ""}}

        Input: {text}

        Use .exe for apps. Output ONLY valid JSON object:
        """
        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )
        content = response["message"]["content"].strip()
        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end > start:
            return json.loads(content[start:end])
        else:
            logger.warning("No JSON in LLM response")
            return None
    except Exception as e:
        logger.error(f"LLM intent parsing failed: {e}")
        return None

def get_intent(text: str):
    """Try LLM parsing first, fallback to keyword-based parsing."""
    intent = llm_parse(text)
    if intent is None:
        intent = parse_intent(text)
    return intent