import os
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from google_translate import translate_text  # you already have this module


from ml_advisor import NewCropAdvisor, ExistingCropAdvisor


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


# ---------------- DEFAULT ROOT ----------------
@app.get("/")
def root():
    return {"status": "ok", "message": "Crop advisory backend running"}


# ---------------- EXISTING CROP POST API ----------------
@app.post("/advice/existing")
async def existing_crop_advice(request: ExistingCropAdviceRequest):
    try:
        logs = request.activityLogs or []
        stage_based_messages = []

        # Quick mapping by subActivity if exists
        for log in logs:
            sub = log.get("subActivity", "")
            if sub in existing_rules:
                stage_based_messages.append(existing_rules[sub])

        # If nothing matched → provide fallback based on farm details
        if not stage_based_messages:
            crop = request.farmDetails.get("cropName", "your crop")
            stage_based_messages.append([
                f"Maintain irrigation based on soil moisture for {crop}.",
                f"Apply balanced fertilizer based on recent soil test.",
                "Monitor pest symptoms weekly.",
                "Ensure proper drainage to avoid root rot."
            ])

        # Format response
        return {
            "cropName": request.farmDetails.get("cropName", "Crop"),
            "cropManagement": stage_based_messages[0],
            "nutrientManagement": stage_based_messages[0],
            "waterManagement": stage_based_messages[0],
            "protectionManagement": stage_based_messages[0],
            "harvestMarketing": stage_based_messages[0]
        }

    except Exception as e:
        return {
            "cropName": "Crop",
            "cropManagement": ["General management recommendations available."],
            "nutrientManagement": ["General nutrient recommendations available."],
            "waterManagement": ["Ensure regular irrigation based on crop needs."],
            "protectionManagement": ["Monitor pest symptoms & act accordingly."],
            "harvestMarketing": ["Harvest at maturity & follow market standards."]
        }



# ---------------- NEW CROP POST API ----------------
@app.post("/advice/new", response_model=NewCropResponse)
def get_new_crop_advice(req: NewCropRequest):
    try:
        # Get ML recommendations in English
        recs = new_crop_advisor.recommend(req.dict())
        
        # Auto-translate if language is not English (e.g., 'kn' for Kannada)
        lang = (req.language or "en").lower()
        if lang != "en":
            for r in recs:
                for key in ("waterManagement", "nutrientManagement", "seedSelection", "otherAdvice"):
                    r[key] = translate_text(r[key], target_language=lang)

        return {"recommendations": recs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# -------------- FRIENDLY GET (NEW CROP) ----------------
@app.get("/advice/new")
def info_new():
    return {
        "message": "This endpoint only supports POST method.",
        "usage": "Send POST /advice/new with JSON to get crop recommendations.",
        "sample_body": {
            "district": "Uttara Kannada",
            "taluk": "Sirsi",
            "soilType": "Red Soil",
            "farmSizeAcre": 1.0,
            "avgRainfall": 2300,
            "avgTemp": 27
        },
        "note": "This endpoint is meant for API/Android usage, not for direct browser access."
    }


