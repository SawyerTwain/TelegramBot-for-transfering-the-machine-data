import json
import os
from typing import Dict

class LanguageManager:
    LANGUAGE_FILE = "user_languages.json"

    @classmethod
    def _load_languages(cls) -> Dict[str, str]: #loads dictionary if exists
        if os.path.exists(cls.LANGUAGE_FILE):
            try:
                with open(cls.LANGUAGE_FILE, "r", encoding="utf-8") as f: #using with to ensure that the file will be closed after we use it
                    return json.load(f) #reads all the json from a file and turns it into a python dict
            except (json.JSONDecodeError, IOError) as e: #input/output error
                print(f"⚠️ Error by loading {cls.LANGUAGE_FILE}: {e}")
        return {}

    @classmethod
    def _save_languages(cls, data: Dict[str, str]) -> None: #saves the dictionary into the file
        try:
            with open(cls.LANGUAGE_FILE, "w", encoding="utf-8") as f: 
                json.dump(data, f, ensure_ascii=False, indent=2) #ensure_ascii=False - so we can save german letters, indent=2 - formates the file with spaces
        except IOError as e:
            print(f"❌ Error by saving {cls.LANGUAGE_FILE}: {e}")

    @classmethod
    def get_lang(cls, user_id: int) -> str: #returns users chosen language (def English)
        data = cls._load_languages()
        return data.get(str(user_id), "en")

    @classmethod
    def set_lang(cls, user_id: int, language: str) -> None: #sets users language
        if language not in ["en", "de"]:
            raise ValueError("Unsupported language: must be 'en' or 'de'")

        data = cls._load_languages()
        data[str(user_id)] = language
        cls._save_languages(data)

