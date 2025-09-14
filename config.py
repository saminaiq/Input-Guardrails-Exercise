# config.py

# OpenAI API key 
OPENAI_API_KEY = ""

# Input Guardrails Settings
MAX_INPUT_CHARS = 500

DISALLOWED_KEYWORDS = [
    "kill",
    "bomb",
    "terror",
    "hack",
    "illegal",
]

SENSITIVE_PATTERNS = [
    r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",   # email
    r"\b(?:\d[ -]*?){13,16}\b",                          # card numbers
]

AUTO_SANITIZE_PROFANITY = True
BLOCK_ON_SENSITIVE = True
BLOCK_ON_DISALLOWED = True


