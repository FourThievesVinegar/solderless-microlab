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
        A dict with translation strings.

    Raises:
        FileNotFoundError: if neither lang_code nor DEFAULT_LANG file exists.
    """
    # init cache dict on function
    cache = getattr(load_translation, '_cache', {})

    # if not reloading and we already have it, return cached
    if not reload and lang_code in cache:
        return cache[lang_code]

    # build candidate file paths: preferred then fallback
    candidates = [
        os.path.join(BASE_PATH, lang_code, 'strings.json'),
        os.path.join(BASE_PATH, DEFAULT_LANG, 'strings.json'),
    ]

    for path in candidates:
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            cache[lang_code] = data
            load_translation._cache = cache
            return data

    # none found
    raise FileNotFoundError(f"No translation file for '{lang_code}', and fallback '{DEFAULT_LANG}' not found.")
