import json
import os

BASE_PATH = os.path.join(os.path.dirname(__file__), "locales")
DEFAULT_LANG = "en"

def load_translation(lang_code):
    lang_path = os.path.join(BASE_PATH, lang_code, "strings.json")
    fallback_path = os.path.join(BASE_PATH, DEFAULT_LANG, "strings.json")

    try:
        with open(lang_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        with open(fallback_path, 'r', encoding='utf-8') as f:
            return json.load(f)
