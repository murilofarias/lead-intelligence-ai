"""Security helpers: rate limiting, prompt-injection sanitization, PII redaction."""
from __future__ import annotations

import re

from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.config import get_settings

settings = get_settings()

limiter = Limiter(key_func=get_remote_address, default_limits=[settings.rate_limit])

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w.-]+\.\w+")
_PHONE_RE = re.compile(r"\+?\d[\d\s().-]{7,}\d")
_CONTROL_RE = re.compile(r"[\x00-\x08\x0b-\x1f\x7f]")


def redact_pii(text: str) -> str:
    """Redact emails / phone numbers from a string for safe logging."""
    text = _EMAIL_RE.sub("[email]", text)
    text = _PHONE_RE.sub("[phone]", text)
    return text


def sanitize_user_input(text: str, max_length: int = 4000) -> str:
    """Defend against prompt injection:
    - strip control characters
    - truncate to a safe size
    - escape XML-like sentinel tags we use for data boundaries
    The LLM system prompt is instructed to treat content inside <lead> tags as data only.
    """
    text = _CONTROL_RE.sub("", text or "")
    text = text.replace("</lead>", "&lt;/lead&gt;").replace("<lead>", "&lt;lead&gt;")
    if len(text) > max_length:
        text = text[:max_length] + "…"
    return text
