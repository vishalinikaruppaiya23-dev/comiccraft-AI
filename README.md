# ComicCraft — corrected Windows-friendly version

ComicCraft is a FastAPI web app that creates a five-panel comic from a story idea.

## What was fixed

- Removed the mandatory Stable Diffusion/PyTorch dependency. No GPU is required.
- Replaced the deprecated `google-generativeai` SDK with Google's `google-genai` SDK.
- Gemini model is configurable through `.env` instead of being hard-coded.
- Added local fallbacks so the app still runs without an API key.
- Added `/health` endpoint.
- Improved JSON extraction and validation.
- Added Windows-friendly font handling and lightweight local comic artwork.
- Kept PDF export and the JSON API.

## 1. Open the correct folder

After extracting the ZIP, open PowerShell in the folder that contains:

```text
app\
templates\
static\requirements.txt
```

For example:

```powershell
cd C:\Users\YOUR_NAME\Downloads\ComicCraft\comiccraft
```

## 2. Create the virtual environment

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If `py` is unavailable, use `python` instead.

## 3. Optional Gemini setup

Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```

Open `.env` and put your Google AI Studio API key in `GEMINI_API_KEY`.

The app still works without the key; it uses local fallback story text and local artwork.

If your account exposes another current Gemini model, change `GEMINI_MODEL` accordingly.

## 4. Start ComicCraft

```powershell
python -m uvicorn app.main:app --reload
```

Open:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/health
- http://127.0.0.1:8000/docs

Do **not** open `0.0.0.0:8000` in the browser. `0.0.0.0` is a server bind address; use `127.0.0.1` in your browser.

## 5. Test image generation

Open:

http://127.0.0.1:8000/test-image?prompt=A%20hero%20in%20a%20forest

## Architecture

```text
Browser
  ↓
FastAPI
  ├── Gemini (optional) → outline + narration
  ├── Pillow → lightweight local comic artwork
  └── FPDF2 → downloadable PDF
```

This version deliberately avoids downloading a multi-GB Stable Diffusion model just to start the application. A separate image API can be added later if you want fully AI-generated artwork.


Windows clean start:
1. Run `run_windows.bat` from this folder. It recreates `.venv` so incompatible Starlette versions cannot remain.
2. Open http://127.0.0.1:8000
