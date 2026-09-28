"""Lightweight comic artwork generator.

No Stable Diffusion/PyTorch is required. By default it creates attractive
comic-panel artwork locally with Pillow. An external image provider can be
added later without changing the rest of the app.
"""
import re
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PANELS_DIR = Path(__file__).resolve().parent.parent.parent / "static" / "panels"
PANELS_DIR.mkdir(parents=True, exist_ok=True)


def _font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def _filename(prompt, panel_number):
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", prompt.lower()).strip("_")[:45] or "scene"
    return f"panel_{panel_number}_{slug}.png"


def _draw(prompt, panel_number, size=(1000, 650)):
    backgrounds = [(236, 246, 255), (255, 244, 224), (238, 250, 238), (248, 238, 250), (255, 239, 239)]
    img = Image.new("RGB", size, backgrounds[(panel_number - 1) % len(backgrounds)])
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((18, 18, size[0]-18, size[1]-18), radius=22, outline=(35, 35, 45), width=7)
    d.rectangle((35, 35, size[0]-35, 100), fill=(35, 35, 45))
    d.text((60, 52), f"COMICCRAFT • PANEL {panel_number}", fill="white", font=_font(30, True))
    # simple scene illustration: sun, ground, character bubble
    d.ellipse((size[0]-180, 125, size[0]-80, 225), fill=(250, 205, 80), outline=(35,35,45), width=4)
    d.polygon([(60, size[1]-100), (250, 330), (430, size[1]-100)], fill=(130, 180, 135), outline=(35,35,45))
    cx, cy = 500, 390
    d.ellipse((cx-70, cy-95, cx+70, cy+45), fill=(244, 196, 160), outline=(35,35,45), width=5)
    d.ellipse((cx-48, cy-55, cx-30, cy-35), fill=(30,30,30))
    d.ellipse((cx+30, cy-55, cx+48, cy-35), fill=(30,30,30))
    d.arc((cx-35, cy-10, cx+35, cy+30), 0, 180, fill=(30,30,30), width=4)
    d.line((cx-55, cy+45, cx-90, size[1]-100), fill=(35,35,45), width=12)
    d.line((cx+55, cy+45, cx+90, size[1]-100), fill=(35,35,45), width=12)
    d.rounded_rectangle((70, 125, 580, 255), radius=20, fill="white", outline=(35,35,45), width=4)
    wrapped = textwrap.fill(prompt, width=55)
    d.multiline_text((95, 150), wrapped, fill=(35,35,45), font=_font(22), spacing=6)
    return img


def generate_image(image_prompt: str, panel_number: int) -> str:
    output = PANELS_DIR / _filename(image_prompt, panel_number)
    _draw(image_prompt, panel_number).save(output, "PNG")
    return str(output.relative_to(PANELS_DIR.parent.parent))
