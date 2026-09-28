"""
layout_builder.py
------------------
Organizes the generated outline, narration/dialogue, and illustrations into
a single structured layout that the frontend templates and PDF exporter can
both consume directly.
"""

from typing import Dict, List


def build_comic_layout(outline: List[Dict], story: Dict, image_paths: Dict[int, str]) -> List[Dict]:
    """
    Merge outline + story + images into one ordered list of panel dicts:

        {
            "panel_number": int,
            "title": str,
            "scene_description": str,
            "image_prompt": str,
            "image_path": str,
            "caption": str,
            "narration": str,
        }
    """
    layout = []
    for panel in sorted(outline, key=lambda p: p["panel_number"]):
        num = panel["panel_number"]
        story_entry = story.get(num, {})
        layout.append(
            {
                "panel_number": num,
                "title": panel.get("title", f"Panel {num}"),
                "scene_description": panel.get("scene_description", ""),
                "image_prompt": panel.get("image_prompt", ""),
                "image_path": image_paths.get(num, ""),
                "caption": story_entry.get("caption", ""),
                "narration": story_entry.get("narration", ""),
            }
        )
    return layout
