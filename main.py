from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from ml_advisor import NewCropAdvisor, ExistingCropAdvisor
from google_translate import translate_text


app = FastAPI(title="Crop Advisory Backend")

new_crop_advisor = NewCropAdvisor()
existing_crop_advisor = ExistingCropAdvisor()


# ============== MODELS =================
class FarmDetails(BaseModel):
    cropName: Optional[str] = None
    district: Optional[str] = None
    taluk: Optional[str] = None
    soilType: Optional[str] = None


class ExistingCropRequest(BaseModel):
    userId: str
    primaryCropKey: str
    farmDetails: FarmDetails
    activityLogs: List[Dict]
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
    language: Optional[str] = "en"


class NewCropAdvice(BaseModel):
    cropName: str
    score: float
    waterManagement: str
    nutrientManagement: str
    seedSelection: str
    otherAdvice: str


class NewCropResponse(BaseModel):
    recommendations: List[NewCropAdvice]


# ============ KNOWLEDGE BASE FOR KARNATAKA =================
locality_crops = {
    "uttara kannada": ["areca nut", "pepper", "paddy", "banana", "turmeric"],
    "belagavi": ["sugarcane", "soybean", "maize", "paddy", "wheat"],
    "shivamogga": ["areca nut", "pepper", "paddy", "banana", "ginger"],
    "dharwad": ["soybean", "cotton", "maize", "groundnut", "sunflower"],
    "haveri": ["cotton", "chilli", "maize", "paddy", "jowar"],
    "ballari": ["pomegranate", "groundnut", "sunflower", "cotton"],
    "chikkamagaluru": ["coffee", "pepper", "areca nut", "banana"],
    "mysuru": ["cotton", "ragi", "paddy", "groundnut", "sugarcane"],
    "mandya": ["sugarcane", "paddy", "mulberry", "banana"],
    "tumakuru": ["ragi", "groundnut", "pigeon pea", "tomato"],
}

soil_crops = {
    "red soil": ["areca nut", "pepper", "cotton", "groundnut", "ragi", "paddy"],
    "black soil": ["cotton", "soybean", "turmeric", "paddy", "banana"],
    "laterite": ["areca nut", "pepper", "coffee", "banana"],
    "alluvial": ["paddy", "sugarcane", "banana", "vegetables"],
    "sandy": ["groundnut", "onion", "melon", "cucumber"],
}

temp_range = {
    "areca nut": (18, 32), "pepper": (20, 30), "coffee": (15, 28),
    "banana": (15, 35), "cotton": (22, 32), "soybean": (20, 32),
    "maize": (20, 32), "paddy": (18, 38), "groundnut": (20, 36),
    "turmeric": (20, 30), "sugarcane": (20, 35),
}

rainfall_range = {
    "areca nut": (2000, 3500), "pepper": (2000, 3000), "coffee": (1800, 3000),
    "paddy": (900, 2500), "cotton": (600, 1200), "soybean": (700, 1200),
    "maize": (500, 900), "groundnut": (500, 1200), "banana": (1100, 3000),
    "turmeric": (900, 1800), "sugarcane": (1100, 2200),
}


# ================ EXISTING CROP ADVICE =================
@app.post("/advice/existing", response_model=ExistingCropResponse)
def existing_crop_advice(req: ExistingCropRequest):
    try:
        result = existing_crop_advisor.advise(req.activityLogs, req.farmDetails.dict())
        lang = req.language.lower()

        if lang != "en":
            for key in result:
                if isinstance(result[key], list):
                    result[key] = [translate_text(x, target_language=lang) for x in result[key]]

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ================ NEW CROP ADVICE =================
@app.post("/advice/new", response_model=NewCropResponse)
def new_crop_advice(req: NewCropRequest):
    try:
        base_recs = new_crop_advisor.recommend(req.dict(), top_k=6)

        district = req.district.lower()
        soil = req.soilType.lower()
        rain = req.avgRainfall
        temp = req.avgTemp

        ranked = []
        for r in base_recs:
            crop = r["cropName"].lower()
            score = r["score"]

            # Knowledge-base boosting
            if district in locality_crops and crop in locality_crops[district]:
                score += 0.35
            if soil in soil_crops and crop in soil_crops[soil]:
                score += 0.30
            if crop in temp_range:
                lo, hi = temp_range[crop]
                if lo <= temp <= hi:
                    score += 0.20
            if crop in rainfall_range:
                lo, hi = rainfall_range[crop]
                if lo <= rain <= hi:
                    score += 0.25

            r["score"] = round(score, 3)
            ranked.append(r)

        ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)[:4]

        if req.language.lower() != "en":
            for r in ranked:
                for key in ("waterManagement", "nutrientManagement", "seedSelection", "otherAdvice"):
                    r[key] = translate_text(r[key], target_language=req.language)

        return {"recommendations": ranked}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"status": "running", "message": "Crop advisory backend active"}
