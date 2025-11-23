import os
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

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
@app.post("/advice/existing", response_model=ExistingCropResponse)
def get_existing_crop_advice(req: ExistingCropRequest):
    try:
        advice = existing_crop_advisor.advise(req.activityLogs, req.farmDetails.dict())
        return advice
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------- FRIENDLY GET (EXISTING CROP) ----------------
@app.get("/advice/existing")
def info_existing():
    return {
        "message": "This endpoint only supports POST method.",
        "usage": "Send POST /advice/existing with farm details + activity logs to get advisory.",
        "note": "This endpoint is intended for your Android application, not direct browser access."
    }


# ---------------- NEW CROP POST API ----------------
@app.post("/advice/new", response_model=NewCropResponse)
def get_new_crop_advice(req: NewCropRequest):
    try:
        rec = new_crop_advisor.recommend(req.dict())
        return {"recommendations": rec}
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
