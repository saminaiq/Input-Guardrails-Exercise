# guardrails.py
from config import OPENAI_API_KEY
import openai

openai.api_key = OPENAI_API_KEY

import re
from better_profanity import profanity
from config import (
    MAX_INPUT_CHARS,
    DISALLOWED_KEYWORDS,
    SENSITIVE_PATTERNS,
    AUTO_SANITIZE_PROFANITY,
    BLOCK_ON_SENSITIVE,
    BLOCK_ON_DISALLOWED,
)

profanity.load_censor_words()

def _contains_disallowed_keywords(text: str):
    found = []
    for kw in DISALLOWED_KEYWORDS:
        if kw.lower() in text.lower():
            found.append(kw)
    return found

def _matches_sensitive_patterns(text: str):
    found = []
    for pat in SENSITIVE_PATTERNS:
        if re.search(pat, text):
            found.append(pat)
    return found

def _sanitize_sensitive(text: str):
    text = re.sub(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", "[redacted_email]", text)
    text = re.sub(r"\b(?:\d[ -]*?){13,16}\b", "[redacted_number]", text)
    return text

def _sanitize_profanity(text: str):
    return profanity.censor(text)

def validate_input(text: str):
    """
    Returns: (allowed, reasons, sanitized_text)
    """
    reasons = []
    sanitized = text

    if not text.strip():
        return False, ["empty_input"], ""

    if len(text) > MAX_INPUT_CHARS:
        reasons.append("too_long")

    dks = _contains_disallowed_keywords(text)
    if dks:
        reasons.append("disallowed_keywords: " + ", ".join(dks))

    sps = _matches_sensitive_patterns(text)
    if sps:
        reasons.append("sensitive_data_detected")

    if profanity.contains_profanity(text):
        reasons.append("profanity_detected")
        if AUTO_SANITIZE_PROFANITY:
            sanitized = _sanitize_profanity(sanitized)

    if (dks and BLOCK_ON_DISALLOWED) or (sps and BLOCK_ON_SENSITIVE):
        sanitized = _sanitize_sensitive(sanitized)
        return False, reasons, sanitized

    return (len(reasons) == 0), reasons, _sanitize_sensitive(sanitized)
