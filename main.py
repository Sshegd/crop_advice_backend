# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from ml_advisor import NewCropAdvisor, ExistingCropAdvisor

app = FastAPI(title="Crop Advisory Backend")

new_crop_advisor = NewCropAdvisor()
existing_crop_advisor = ExistingCropAdvisor()

# --------- Pydantic Schemas ---------
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
    activityLogs: List[Dict[str, Any]]   # send flattened list of logs from Android

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

# --------- Routes ---------

@app.get("/")
def root():
    return {"status": "ok", "message": "Crop advisory backend running"}

@app.post("/advice/existing", response_model=ExistingCropResponse)
def get_existing_advice(req: ExistingCropRequest):
    try:
        advice = existing_crop_advisor.advise(req.activityLogs, req.farmDetails.dict())
        return advice
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/advice/new", response_model=NewCropResponse)
def get_new_crop_advice(req: NewCropRequest):
    try:
        recs = new_crop_advisor.recommend(req.dict())
        return {"recommendations": recs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
