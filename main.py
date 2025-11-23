# main.py
import os
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import firebase_admin
from firebase_admin import credentials

from ml_advisor import MLAdvisor
from google_translate import translate_text

# ---------------- FIREBASE INITIALIZATION ---------------- #
if not firebase_admin._apps:
    if "SERVICE_ACCOUNT_KEY" in os.environ:
        # Railway / Render: JSON string in env
        creds_json = json.loads(os.environ["SERVICE_ACCOUNT_KEY"])
        cred = credentials.Certificate(creds_json)
    else:
        # Local fallback – you can keep a file only on your laptop
        if os.path.exists("serviceAccountKey.json"):
            cred = credentials.Certificate("serviceAccountKey.json")
        else:
            cred = None  # Firebase not mandatory for this API

    if cred is not None:
        firebase_admin.initialize_app(cred)

# ---------------- FASTAPI APP + ML ---------------- #
app = FastAPI(title="Crop Advisory Backend", version="1.0.0")
advisor = MLAdvisor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- HELPERS ---------------- #
def maybe_translate(text: str, lang: str) -> str:
    """Translate text using Google only if language != 'en'."""
    if not text:
        return text
    if lang is None or lang.lower().startswith("en"):
        return text
    try:
        return translate_text(text, target_lang=lang)
    except Exception:
        # If translation fails, return English version so user still gets advice
        return text


# ---------------- BASIC ROUTES ---------------- #
@app.get("/")
async def root():
    return {"message": "Crop Advisory Backend is running"}

@app.get("/health")
async def health():
    return {"status": "ok", "models_loaded": advisor.models_loaded()}


# ---------------- EXISTING CROP ADVICE ---------------- #
@app.post("/advice/existing")
async def advice_existing(payload: dict):
    """
    Expected body:
    {
      "cropName": "areca nut",
      "stage": "planting_cultivation",
      "logs": [...],           # list of log dicts from Firebase
      "language": "en" | "kn"
    }
    """
    crop_name = payload.get("cropName", "")
    stage = payload.get("stage", "")
    logs = payload.get("logs", [])
    lang = payload.get("language", "en")

    base, recs = advisor.existing_crop_advice(
        crop_name=crop_name,
        stage=stage,
        logs=logs
    )

    base = maybe_translate(base, lang)
    recs = [maybe_translate(r, lang) for r in recs]

    return {
        "success": True,
        "crop": crop_name,
        "stage": stage,
        "advisory": base,
        "recommendations": recs
    }


# ---------------- NEW CROP RECOMMENDATION ---------------- #
@app.post("/advice/new")
async def advice_new(payload: dict):
    """
    Expected body:
    {
      "soilType": "Red Soil",
      "area": "1 acre",
      "district": "Uttara Kannada",
      "weather": {...optional...},
      "language": "en" | "kn"
    }
    """
    lang = payload.get("language", "en")

    base, recs, crop = advisor.new_crop_recommend(payload)

    base = maybe_translate(base, lang)
    recs = [maybe_translate(r, lang) for r in recs]

    return {
        "success": True,
        "bestCrop": crop,
        "advisory": base,
        "recommendations": recs
    }


# --------------- PORT FOR RAILWAY LOCAL TESTING --------- #
# Only needed if you run `python main.py` locally
import uvicorn
import os

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)




