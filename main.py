"""ComicCraft FastAPI entry point."""
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

from app.routes import router  # noqa: E402

app = FastAPI(title="ComicCraft", description="AI Comic Story Creator", version="2.0.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ComicCraft"}
