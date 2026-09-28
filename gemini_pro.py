"""Comic narration generation using the configured Gemini model, with fallback."""
from typing import Dict, List
from app.ai.gemini_client import generate_text, extract_json, get_client


def _prompt(outline, character_name, tone):
    lines = "\n".join(f"Panel {p['panel_number']}: {p['title']} — {p['scene_description']}" for p in outline)
    return f"""Write concise comic captions and dialogue for {character_name}.
Tone: {tone}
Outline:
{lines}

Return ONLY a JSON object keyed by panel number. Each value must have:
caption: one short ambient sentence
narration: 1-2 short sentences of narration/dialogue
"""


def _fallback(outline, character_name, tone):
    return {p["panel_number"]: {
        "caption": f"A {tone} moment unfolds.",
        "narration": f"{character_name} takes a breath and keeps moving forward.",
    } for p in outline}


def generate_story(outline: List[Dict], character_name: str, tone: str) -> Dict:
    if get_client() is None:
        return _fallback(outline, character_name, tone)
    try:
        raw = extract_json(generate_text(_prompt(outline, character_name, tone)))
        result = {}
        for p in outline:
            entry = raw.get(str(p["panel_number"]), {}) if isinstance(raw, dict) else {}
            result[p["panel_number"]] = {
                "caption": str(entry.get("caption", "")),
                "narration": str(entry.get("narration", "")),
            }
        return result
    except Exception as exc:
        print(f"[gemini_pro] fallback: {exc}")
        return _fallback(outline, character_name, tone)
