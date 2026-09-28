"""Comic outline generation using the modern Gemini SDK, with fallback."""
from typing import Dict, List
from app.ai.gemini_client import generate_text, extract_json, get_client

NUM_PANELS = 5


def _prompt(story_prompt, character_name, setting, tone, art_style):
    return f"""Create exactly {NUM_PANELS} sequential comic panels.
Story idea: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Return ONLY a JSON array. Each object must contain:
panel_number, title, scene_description, image_prompt.
Make the same character visually consistent across all panels.
"""


def _fallback(story_prompt, character_name, setting, tone, art_style):
    beats = [
        ("The Beginning", f"{character_name} begins an adventure in {setting}."),
        ("The Discovery", f"{character_name} discovers an unexpected clue."),
        ("The Challenge", f"A difficult challenge appears and tests {character_name}."),
        ("The Turning Point", f"{character_name} makes a brave decision."),
        ("The Resolution", f"{character_name} reaches a satisfying ending."),
    ]
    return [{
        "panel_number": i,
        "title": title,
        "scene_description": f"{description} The story idea is: {story_prompt}",
        "image_prompt": f"{art_style} comic illustration, {setting}, {tone} mood, main character {character_name}, {description}",
    } for i, (title, description) in enumerate(beats, 1)]


def generate_outline(story_prompt: str, character_name: str, setting: str, tone: str, art_style: str) -> List[Dict]:
    if get_client() is None:
        return _fallback(story_prompt, character_name, setting, tone, art_style)
    try:
        data = extract_json(generate_text(_prompt(story_prompt, character_name, setting, tone, art_style)))
        if not isinstance(data, list) or len(data) < NUM_PANELS:
            raise ValueError("Gemini returned fewer than 5 panels")
        return [{
            "panel_number": i,
            "title": str(item.get("title") or f"Panel {i}"),
            "scene_description": str(item.get("scene_description") or ""),
            "image_prompt": str(item.get("image_prompt") or story_prompt),
        } for i, item in enumerate(data[:NUM_PANELS], 1)]
    except Exception as exc:
        print(f"[gemini_flash] fallback: {exc}")
        return _fallback(story_prompt, character_name, setting, tone, art_style)
