CYRILLIC_TO_LATIN = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "yo", "ж": "zh",
    "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m", "н": "n", "о": "o",
    "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ф": "f", "х": "h", "ц": "ts",
    "ч": "ch", "ш": "sh", "щ": "sht", "ъ": "a", "ы": "iy", "ь": "y", "э": "e", "ю": "yu",
    "я": "ya"
}


def transliterate(text):
    text = text or ''
    return ''.join(CYRILLIC_TO_LATIN.get(ch, ch) for ch in text.lower())
