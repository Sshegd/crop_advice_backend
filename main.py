import os
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from ml_advisor import NewCropAdvisor, ExistingCropAdvisor
from google_translate import translate_text


# ---------------- FASTAPI APP ----------------
app = FastAPI(title="Crop Advisory Backend")

# ---------------- LOAD ML ADVISORS ----------------
new_crop_advisor = NewCropAdvisor()
existing_crop_advisor = ExistingCropAdvisor()


# ---------------- Pydantic Models ----------------
class FarmDetails(BaseModel):
    acre: Optional[str] = None
    ana: Optional[str] = None
    gunta: Optional[str] = None
    cropName: Optional[str] = None
    district: Optional[str] = None
    taluk: Optional[str] = None
    soilType: Optional[str] = None
    harvestPeriod: Optional[str] = None


class ExistingCropRequest(BaseModel):
    userId: str
    primaryCropKey: str = "primary_crop"
    farmDetails: FarmDetails
    activityLogs: List[Dict[str, Any]]
    language: Optional[str] = "en"


class ExistingCropResponse(BaseModel):
    cropName: str
    cropManagement: List[str]
    nutrientManagement: List[str]
    waterManagement: List[str]
    protectionManagement: List[str]
    harvestMarketing: List[str]


class NewCropRequest(BaseModel):
    district: str
    taluk: str
    soilType: str
    farmSizeAcre: float
    avgRainfall: float
    avgTemp: float
    language: Optional[str] = "en"  # "en", "kn", etc.


class NewCropAdvice(BaseModel):
    cropName: str
    score: float
    waterManagement: str
    nutrientManagement: str
    seedSelection: str
    otherAdvice: str


class NewCropResponse(BaseModel):
    recommendations: List[NewCropAdvice]


# ---------------- KNOWLEDGE BASE (Karnataka) ----------------

# District-wise major crops (expandable)
locality_db: Dict[str, List[str]] = {
    "uttara kannada": ["areca nut", "pepper", "paddy", "banana", "turmeric"],
    "belagavi": ["sugarcane", "soybean", "maize", "paddy", "chilli", "wheat"],
    "haveri": ["cotton", "maize", "paddy", "chilli", "jowar"],
    "dharwad": ["cotton", "soybean", "maize", "groundnut", "sunflower"],
    "bagalkote": ["pomegranate", "grapes", "maize", "sorghum", "cotton"],
    "vijayapura": ["pomegranate", "banana", "grapes", "maize", "cotton"],
    "kalaburagi": ["turmeric", "pigeon pea", "cotton", "groundnut", "jowar"],
    "yadgir": ["pigeon pea", "jowar", "sunflower", "groundnut", "paddy"],
    "ballari": ["cotton", "groundnut", "sunflower", "maize", "pomegranate"],
    "tumakuru": ["ragi", "groundnut", "banana", "tomato", "pigeon pea"],
    "chikkamagaluru": ["coffee", "pepper", "areca nut", "cardamom", "banana"],
    "shivamogga": ["areca nut", "pepper", "paddy", "banana", "ginger"],
    "hassan": ["coffee", "pepper", "banana", "ginger", "paddy"],
    "chitradurga": ["groundnut", "ragi", "sunflower", "cotton", "onion"],
    "kodagu": ["coffee", "pepper", "cardamom", "banana", "orange"],
    "mysuru": ["cotton", "ragi", "paddy", "groundnut", "sugarcane"],
    "mandya": ["sugarcane", "paddy", "ragi", "mulberry", "tomato"],
    "ramanagara": ["ragi", "mulberry", "tomato", "banana", "groundnut"],
    "bengaluru rural": ["ragi", "tomato", "beans", "mulberry", "flowers"],
    "bengaluru urban": ["vegetables", "flowers", "mulberry", "millets"],
    "koppal": ["cotton", "groundnut", "maize", "paddy", "chilli"],
    "gadag": ["jowar", "maize", "pigeon pea", "groundnut", "chilli"],
    "kolar": ["mulberry", "mango", "papaya", "tomato", "flowers"],
    "bidar": ["turmeric", "pigeon pea", "cotton", "sugarcane", "soybean"],
}

# Soil-wise suitability
soil_suitability: Dict[str, List[str]] = {
    "red soil": ["areca nut", "pepper", "cotton", "groundnut", "ragi", "paddy", "turmeric"],
    "black soil": ["cotton", "soybean", "turmeric", "paddy", "sugarcane", "banana"],
    "laterite soil": ["areca nut", "pepper", "coffee", "banana", "cardamom"],
    "alluvial soil": ["paddy", "sugarcane", "vegetables", "banana"],
    "sandy soil": ["groundnut", "watermelon", "onion", "cucumber"],
    "silty soil": ["vegetables", "wheat", "paddy", "peas"],
}

# Temperature preference (°C) per crop
temp_pref: Dict[str, tuple] = {
    "areca nut": (18, 32),
    "pepper": (20, 30),
    "coffee": (15, 28),
    "banana": (15, 35),
    "cotton": (22, 32),
    "soybean": (20, 32),
    "maize": (20, 32),
    "paddy": (18, 38),
    "jowar": (20, 32),
    "ragi": (20, 30),
    "groundnut": (20, 36),
    "turmeric": (20, 30),
    "ginger": (20, 28),
    "sugarcane": (20, 35),
    "pomegranate": (18, 35),
    "grapes": (15, 32),
    "sunflower": (20, 30),
    "pigeon pea": (22, 34),
    "mulberry": (20, 32),
    "tomato": (15, 30),
}

# Rainfall preference (mm/year) per crop
rain_pref: Dict[str, tuple] = {
    "areca nut": (2000, 3500),
    "pepper": (2000, 3000),
    "coffee": (1800, 3000),
    "paddy": (900, 2500),
    "cotton": (600, 1200),
    "soybean": (700, 1200),
    "maize": (500, 900),
    "jowar": (400, 700),
    "ragi": (400, 900),
    "groundnut": (500, 1200),
    "turmeric": (900, 1800),
    "pomegranate": (500, 900),
    "banana": (1100, 3000),
    "sugarcane": (1100, 2200),
    "sunflower": (400, 800),
    "ginger": (1500, 2500),
    "mulberry": (600, 900),
    "tomato": (600, 900),
}


# ---------------- ROOT ----------------
@app.get("/")
def root():
    return {"status": "ok", "message": "Crop advisory backend running"}


# ---------------- EXISTING CROP POST API ----------------
@app.post("/advice/existing", response_model=ExistingCropResponse)
def existing_crop_advice(req: ExistingCropRequest):
    """
    Advisory based on Firebase activity logs + farm details.
    Uses ExistingCropAdvisor from ml_advisor.py
    """
    try:
        advice: Dict[str, Any] = existing_crop_advisor.advise(
            logs=req.activityLogs,
            farm_details=req.farmDetails.dict(),
        )

        # Ensure crop name present
        if not advice.get("cropName"):
            advice["cropName"] = req.farmDetails.cropName or "Crop"

        # Optionally translate if language is not English
        lang = (req.language or "en").lower()
        if lang != "en":
            for key in [
                "cropManagement",
                "nutrientManagement",
                "waterManagement",
                "protectionManagement",
                "harvestMarketing",
            ]:
                translated = []
                for line in advice.get(key, []):
                    translated.append(translate_text(line, target_language=lang))
                advice[key] = translated

        return advice

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ---------------- NEW CROP POST API (location + soil + weather) ----------------
@app.post("/advice/new", response_model=NewCropResponse)
def get_new_crop_advice(req: NewCropRequest):
    """
    New crop recommendation:
    - Uses ML model (NewCropAdvisor) for yield/profit base ranking
    - Boosts scores based on:
        * District (locality_db)
        * Soil type (soil_suitability)
        * Average rainfall (rain_pref)
        * Average temperature (temp_pref)
    """
    try:
        # Get base ML recommendations; each item is a dict:
        # { "cropName": "..", "score": 0.7, "waterManagement": "..", ... }
        recs: List[Dict[str, Any]] = new_crop_advisor.recommend(req.dict())

        district = (req.district or "").strip().lower()
        soil = (req.soilType or "").strip().lower()
        rain = req.avgRainfall
        temp = req.avgTemp

        ranked: List[Dict[str, Any]] = []

        for r in recs:
            crop = r.get("cropName", "").strip().lower()
            score = float(r.get("score", 0.0))

            # 1) Location-based suitability
            if district in locality_db and crop in locality_db[district]:
                score += 0.30

            # 2) Soil-based suitability
            if soil in soil_suitability and crop in soil_suitability[soil]:
                score += 0.25

            # 3) Temperature suitability
            if crop in temp_pref:
                lo_t, hi_t = temp_pref[crop]
                if lo_t <= temp <= hi_t:
                    score += 0.20

            # 4) Rainfall suitability
            if crop in rain_pref:
                lo_r, hi_r = rain_pref[crop]
                if lo_r <= rain <= hi_r:
                    score += 0.25

            r["score"] = round(score, 3)
            ranked.append(r)

        # Sort by updated score and keep top 4
        ranked = sorted(ranked, key=lambda x: x.get("score", 0.0), reverse=True)[:4]

        # Auto-translate advisory text if language != en
        lang = (req.language or "en").lower()
        if lang != "en":
            for r in ranked:
                for key in ("waterManagement", "nutrientManagement", "seedSelection", "otherAdvice"):
                    if r.get(key):
                        r[key] = translate_text(r[key], target_language=lang)

        # Pydantic will validate against NewCropResponse
        return {"recommendations": ranked}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------- FRIENDLY GET (NEW CROP) ----------------
@app.get("/advice/new")
def info_new():
    return {
        "message": "Use POST /advice/new to get crop recommendations.",
        "sample_body": {
            "district": "Uttara Kannada",
            "taluk": "Sirsi",
            "soilType": "Red Soil",
            "farmSizeAcre": 1.0,
            "avgRainfall": 2300,
            "avgTemp": 27,
            "language": "en"
        },
    }
