from loguru import logger
import ollama
import json

def parse_intent(text: str):
    try:
        prompt = f"""
        Extract intent and entity from this user command for a PC assistant.
        Commands like: "open notepad", "open chrome", "open my documents".
        
        Input: {text}
        
        Output ONLY valid JSON:
        {{
            "intent": "open_app|open_file|unknown",
            "entity": "exact app or file name/path"
        }}
        """

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response["message"]["content"].strip()
        # Find JSON object in response
        start = content.find('{')
        end = content.rfind('}') + 1
        json_str = content[start:end]
        
        return json.loads(json_str)

    except Exception as e:
        logger.error(f"Intent parsing failed: {e}")
        return {"intent": "unknown", "entity": ""}
