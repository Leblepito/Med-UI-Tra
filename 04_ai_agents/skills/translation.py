"""
AntiGravity Ventures — Skills: Translation
TR / RU / EN / TH dil algılama ve çeviri yardımcısı.
"""
from __future__ import annotations

import re


LANG_PATTERNS: dict[str, list[str]] = {
    "ru": ["ии", "ение", "ский", "ный", "ство", "ать", "лечение", "отель"],
    "tr": ["ğ", "ş", "ç", "ö", "ü", "ı", "orum", "yor", "mak"],
    "th": ["ก", "ข", "ค", "ง", "จ", "ช", "ซ", "ด"],
    "en": [r"\bthe\b", r"\band\b", r"\bof\b", r"\bfor\b", r"\bwith\b"],
}


def detect_language(text: str) -> str:
    """Metnin dilini tespit eder. Varsayılan: 'en'."""
    scores: dict[str, int] = {lang: 0 for lang in LANG_PATTERNS}
    for lang, patterns in LANG_PATTERNS.items():
        for p in patterns:
            if re.search(p, text, re.IGNORECASE | re.UNICODE):
                scores[lang] += 1
    best = max(scores, key=lambda l: scores[l])
    return best if scores[best] > 0 else "en"


def get_greeting(lang: str) -> str:
    greetings = {
        "ru": "Добро пожаловать в AntiGravity! Как могу помочь?",
        "tr": "AntiGravity'ye hoş geldiniz! Size nasıl yardımcı olabilirim?",
        "en": "Welcome to AntiGravity! How can I help you?",
        "th": "ยินดีต้อนรับสู่ AntiGravity! ฉันจะช่วยอะไรคุณได้บ้าง?",
    }
    return greetings.get(lang, greetings["en"])
