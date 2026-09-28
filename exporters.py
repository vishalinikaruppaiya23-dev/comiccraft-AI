"""
exporters.py
------------
Compiles a finished comic layout into a downloadable, multi-page PDF using
the FPDF library. Each panel's image and narration are placed on their own
page, and the finished file is saved to static/exports/ with a timestamped
filename.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List

from fpdf import FPDF

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXPORTS_DIR = PROJECT_ROOT / "static" / "exports"
EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


def _pdf_text(value) -> str:
    value = str(value or "").replace("—", "-").replace("–", "-").replace("’", "'").replace("•", "*")
    return value.encode("latin-1", errors="replace").decode("latin-1")


class ComicPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "ComicCraft", align="C", ln=True)
        self.ln(2)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def save_pdf(layout: List[Dict], character_name: str = "Comic") -> str:
    """
    Build a multi-page PDF from a comic layout and save it under
    static/exports/. Returns the relative file path to the saved PDF.
    """
    pdf = ComicPDF()
    pdf.set_auto_page_break(auto=True, margin=20)

    for panel in layout:
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 14)
        pdf.multi_cell(0, 10, panel.get("title", f"Panel {panel.get('panel_number', '')}"))
        pdf.ln(2)

        image_path = panel.get("image_path", "")
        if image_path:
            full_image_path = PROJECT_ROOT / image_path
            if full_image_path.exists():
                try:
                    pdf.image(str(full_image_path), w=150)
                    pdf.ln(4)
                except Exception as exc:  # noqa: BLE001
                    print(f"[exporters] Could not embed image {full_image_path}: {exc}")

        if panel.get("scene_description"):
            pdf.set_font("Helvetica", "I", 11)
            pdf.multi_cell(0, 7, _pdf_text(panel["scene_description"]))
            pdf.ln(1)

        if panel.get("caption"):
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 7, f"Caption: {panel['caption']}")
            pdf.ln(1)

        if panel.get("narration"):
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 7, _pdf_text(panel["narration"]))

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = "".join(c for c in character_name if c.isalnum()) or "comic"
    filename = f"{safe_name}_{timestamp}.pdf"
    output_path = EXPORTS_DIR / filename

    pdf.output(str(output_path))

    return str(output_path.relative_to(PROJECT_ROOT))
