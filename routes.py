from pathlib import Path
from urllib.parse import quote
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from app.ai.gemini_flash import generate_outline
from app.ai.gemini_pro import generate_story
from app.ai.image_generator import generate_image
from app.exporters import save_pdf
from app.layout_builder import build_comic_layout
from app.models import PromptRequest

router = APIRouter()
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


def _run_comic_pipeline(story_prompt, character_name, setting, tone, art_style):
    outline = generate_outline(story_prompt, character_name, setting, tone, art_style)
    story = generate_story(outline, character_name, tone)
    image_paths = {p["panel_number"]: generate_image(p["image_prompt"], p["panel_number"]) for p in outline}
    layout = build_comic_layout(outline, story, image_paths)
    pdf_path = save_pdf(layout, character_name)
    return layout, pdf_path


@router.get("/")
async def homepage(request: Request):
    return templates.TemplateResponse(request=request, name="index.html", context={})


@router.post("/generate")
async def generate_comic(request: Request, story_prompt: str = Form(...), character_name: str = Form(...),
                         setting: str = Form(...), tone: str = Form(...), art_style: str = Form(...)):
    try:
        layout, pdf_path = _run_comic_pipeline(story_prompt.strip(), character_name.strip(), setting, tone, art_style)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Comic generation failed: {exc}") from exc
    return templates.TemplateResponse(request=request, name="comic_preview.html", context={
        "layout": layout, "pdf_path": pdf_path,
        "pdf_url": "/" + quote(pdf_path), "character_name": character_name,
    })


@router.post("/generate-comic/json")
async def generate_comic_json(payload: PromptRequest):
    try:
        layout, pdf_path = _run_comic_pipeline(payload.story_prompt, payload.character_name,
                                               payload.setting, payload.tone, payload.art_style)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Comic generation failed: {exc}") from exc
    return JSONResponse({"character_name": payload.character_name, "layout": layout,
                         "pdf_path": pdf_path, "pdf_url": "/" + quote(pdf_path)})


@router.get("/export-success")
async def export_success(request: Request, pdf_path: str = ""):
    return templates.TemplateResponse(request=request, name="export_success.html", context={"pdf_path": pdf_path})


@router.get("/test-image")
async def test_image(prompt: str = "A brave fox exploring an enchanted forest"):
    try:
        path = generate_image(prompt, 0)
        return JSONResponse({"prompt": prompt, "image_path": path, "image_url": "/" + quote(path)})
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Image generation failed: {exc}") from exc
