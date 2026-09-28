"""Modern Gemini client with graceful local fallbacks.

Uses the current google-genai SDK. The app remains usable without an API key.
"""
import json
import os
import re
from typing import Any

try:
    from google import genai
except ImportError:
    genai = None

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash").strip()

_client = None


def get_client():
    global _client
    if _client is not None:
        return _client
    if not GEMINI_API_KEY or genai is None:
        return None
    _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def generate_text(prompt: str) -> str:
    client = get_client()
    if client is None:
        raise RuntimeError("Gemini is not configured. Set GEMINI_API_KEY in .env.")
    response = client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
    text = getattr(response, "text", None)
    if not text:
        raise RuntimeError("Gemini returned an empty response.")
    return text.strip()


def extract_json(text: str) -> Any:
    cleaned = text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        array_match = re.search(r"\[.*\]", cleaned, re.DOTALL)
        object_match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        match = array_match or object_match
        if not match:
            raise ValueError("Gemini response did not contain valid JSON")
        return json.loads(match.group(0))
