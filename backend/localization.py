import json
import os

BASE_PATH = os.path.join(os.path.dirname(__file__), 'locales')
DEFAULT_LANG = 'en'

def load_translation(lang_code: str = DEFAULT_LANG, reload: bool = False) -> dict[str, str]:
    """
    Load and cache translation JSON for a given language.

    Args:
        lang_code: 2-letter language code (e.g. "en", "ua").
        reload:    If True, forces re-reading from disk even if cached.

    Returns:
        A dict with English strings, updated with a desired language translation strings.

    Raises:
        FileNotFoundError: if neither lang_code nor DEFAULT_LANG file exists.
    """
    # init cache dict on function
    if not hasattr(load_translation, '_cache'):
        load_translation._cache = {}
    cache = load_translation._cache

    # if not reloading and we already have it, return cached
    if not reload and lang_code in cache:
        return cache[lang_code]

    # build candidate file paths: default language, followed by a preferred language
    language_codes = (DEFAULT_LANG,) if lang_code == DEFAULT_LANG else (DEFAULT_LANG, lang_code)

    merged: dict[str, str] = {}
    found_any = False
    for code in language_codes:
        path = os.path.join(BASE_PATH, code, 'strings.json')
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                merged.update(json.load(f))
            found_any = True

    if not found_any:
        raise FileNotFoundError(f"No translation files found for '{lang_code}' or default '{DEFAULT_LANG}'.")

    cache[lang_code] = merged
    return merged