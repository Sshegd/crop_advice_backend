import firebase_admin
import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from ml_advisor import NewCropAdvisor, ExistingCropAdvisor
from google_translate import translate_text
from datetime import datetime
from pest_engine import PestEngine
from pest_db_extended import PEST_DB
from district_pest_history import PEST_HISTORY
from typing import List
from firebase_admin import credentials, db
from yield_predioctor import YieldPredictor


firebase_credentials = json.loads(os.environ["FIREBASE_CREDENTIALS"])
firebase_db_url = os.environ["FIREBASE_DB_URL"]

# --------------------------------------------------
# Firebase Init
# --------------------------------------------------
cred = credentials.Certificate(json.loads(os.environ["FIREBASE_CREDENTIALS"]))
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred, {
        "databaseURL": os.environ["FIREBASE_DB_URL"]
    })

firebase_db = db
app = FastAPI(title="KrishiSakhi Crop Advisory")

new_crop_advisor = NewCropAdvisor()
existing_crop_advisor = ExistingCropAdvisor()
pest_engine = PestEngine(
    pest_db=PEST_DB,
    pest_history=PEST_HISTORY,
    firebase_db=firebase_db
)
yield_predictor = YieldPredictor()


# ============== MODELS =================
class FarmDetails(BaseModel):
    cropName: Optional[str] = None
    district: Optional[str] = None
    taluk: Optional[str] = None
    soilType: Optional[str] = None

class SecondaryCropModel(BaseModel):
    cropName: str
    activityLogs: List[Dict] = []


class ExistingCropRequest(BaseModel):
    language: Optional[str] = "en"          # ✅ REQUIRED
    farmDetails: FarmDetails
    activityLogs: List[Dict] = []           # primary crop logs
    secondaryCrops: List[SecondaryCropModel] = []



class ExistingCropResponse(BaseModel):
    cropName: str
    cropManagement: List[str]
    nutrientManagement: List[str]
    waterManagement: List[str]
    protectionManagement: List[str]
    harvestMarketing: List[str]
    marketPrice: Optional[str] = None
    estimatedNetProfitPerAcre: Optional[str] = None


class ExistingCropFullResponse(BaseModel):
    primaryCropAdvice: ExistingCropResponse
    secondaryCropsAdvice: List[ExistingCropResponse]
# --------------------------------------------------
# ML-LIKE ADVISOR (Lightweight but smart)
# --------------------------------------------------
def infer_crop_name(logs: List[Dict]) -> str:
    for l in logs:
        if "cropName" in l:
            return l["cropName"].title()
    return "Unknown Crop"
    
def stage_based_advice(stage: str, crop: str) -> Dict[str, List[str]]:
    return {
        "cropManagement": [f"{crop}: Continue proper field operations at {stage} stage."],
        "nutrientManagement": [f"Apply nutrients suitable for {stage} stage."],
        "waterManagement": [f"Maintain soil moisture for {stage} stage."],
        "protectionManagement": [f"Monitor pests during {stage} stage."],
        "harvestMarketing": [f"Plan harvest & market linkage early."]
    }

def generate_advice(logs: List[Dict]) -> Dict:
    crop = infer_crop_name(logs)
    stages = set(l.get("stage") for l in logs if l.get("stage"))

    advice = {
        "cropName": crop,
        "cropManagement": [],
        "nutrientManagement": [],
        "waterManagement": [],
        "protectionManagement": [],
        "harvestMarketing": []
    }

    if not stages:
        advice["cropManagement"].append(
            "Add farm activities to receive personalized advice."
        )
        return advice

    for stage in stages:
        a = stage_based_advice(stage, crop)
        for k in advice:
            if k != "cropName":
                advice[k].extend(a[k])

    return advice

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
    avgMarketPricePerQuintal: Optional[int] = None
    expectedYieldPerAcreQuintal: Optional[int] = None
    estimatedNetProfitPerAcre: Optional[int] = None
    priceSource: Optional[str] = None


class NewCropResponse(BaseModel):
    recommendations: List[NewCropAdvice]


class PestRiskRequest(BaseModel):
    userId: str
    language: Optional[str] = "en"
    

class PestAlert(BaseModel):
    cropName: str
    pestName: str
    riskLevel: str
    score: float
    reasons: List[str]
    symptoms: str
    preventive: str
    corrective: str

class PestRiskResponse(BaseModel):
    alerts: List[PestAlert]


class YieldPredictionRequest(BaseModel):
    cropName: str
    district: str
    farmSizeAcre: float
    avgRainfall: float
    avgTemp: float
    language: Optional[str] = "en"


class YieldPredictionResponse(BaseModel):
    cropName: str
    expectedYieldPerAcre: float
    totalExpectedYield: float
    confidence: str
    explanation: str

    
def get_user_crops(firebase_db, user_id: str):
    ref = firebase_db.reference(f"Users/{user_id}")
    user = ref.get()

    if not user:
        return []

    crops = []

    # PRIMARY CROP
    primary_logs = user.get("farmActivityLogs", {})
    farm = user.get("farmDetails", {})

    if primary_logs:
        crops.append({
            "cropName": farm.get("cropName", "Unknown Crop"),
            "activityLogs": list(primary_logs.values())
        })

    # SECONDARY CROPS
    for crop, data in user.get("secondaryCrops", {}).items():
        crops.append({
            "cropName": crop,
            "activityLogs": list(data.get("activityLogs", {}).values())
        })

    return crops

def extract_crop_name(logs, fallback="Unknown Crop"):
    for log in logs:
        name = log.get("cropName")
        if name:
            return name.title()
    return fallback

# ====== MARKET PRICE (KARNATAKA MANDI AVERAGE ₹/QUINTAL) ======
# ====== MARKET PRICE (Karnataka Avg ₹/Quintal 2024–25) ======
market_price_ktk = {
    "areca nut": 58000,
    "pepper": 64000,
    "paddy": 3300,
    "rice":3300,
    "sugarcane": 3600,
    "maize": 2300,
    "banana": 1700,
    "ginger": 8800,
    "turmeric": 7600,
    "soybean": 4700,
    "cotton": 6400,
    "groundnut": 6400,
    "ragi": 3300,
    "coffee": 23500,
    "sunflower": 6200,
    "chilli": 11200,
    # Newly added
    "tomato": 1300,
    "potato": 1200,
    "onion": 1500,
    "pomegranate": 7500,
    "mango": 3200,
    "grapes": 3800,
    "black gram": 7600,
    "green gram": 7200,
    "pigeon pea": 6900,
}

# ====== COST OF CULTIVATION PER ACRE (₹) ======
cultivation_cost = {
    "areca nut": 60000,
    "pepper": 50000,
    "paddy": 38000,
    "rice":38000,
    "sugarcane": 78000,
    "maize": 27000,
    "banana": 95000,
    "ginger": 105000,
    "turmeric": 90000,
    "soybean": 25000,
    "cotton": 52000,
    "groundnut": 30000,
    "ragi": 22000,
    "coffee": 120000,
    "sunflower": 24000,
    "chilli": 92000,
    # Newly added
    "tomato": 45000,
    "potato": 50000,
    "onion": 38000,
    "pomegranate": 90000,
    "mango": 65000,
    "grapes": 100000,
    "black gram": 24000,
    "green gram": 22000,
    "pigeon pea": 26000,
}

# ====== YIELD PER ACRE (Quintals) ======
yield_per_acre = {
    "areca nut": 10,
    "pepper": 3,
    "paddy": 22,
    "rice":22,
    "sugarcane": 40,
    "maize": 18,
    "banana": 35,
    "ginger": 65,
    "turmeric": 55,
    "soybean": 7,
    "cotton": 5,
    "groundnut": 9,
    "ragi": 10,
    "coffee": 7,
    "sunflower": 6,
    "chilli": 30,
    # Newly added
    "tomato": 100,
    "potato": 75,
    "onion": 80,
    "pomegranate": 30,
    "mango": 55,
    "grapes": 60,
    "black gram": 5,
    "green gram": 5,
    "pigeon pea": 6,
}

# ====== English → Kannada Crop Names ======
CROP_NAME_KN = {
    "areca nut": "ಅಡಿಕೆ",
    "banana": "ಬಾಳೆ",
    "paddy": "ಅಕ್ಕಿ",
    "rice":"ಅಕ್ಕಿ",
    "pepper": "ಮೆಣಸು",
    "turmeric": "ಅರಿಶಿನ",
    "ginger": "ಶುಂಠಿ",
    "sugarcane": "ಕಬ್ಬು",
    "groundnut": "ಶೇಂಗಾ",
    "maize": "ಮೆಕ್ಕೆಜೋಳ",
    "ragi": "ರಾಗಿ",
    "cotton": "ಹತ್ತಿ",
    "soybean": "ಸೋಯಾಬೀನ್",
    "coffee": "ಕಾಫಿ",
    "sunflower": "ಸೂರ್ಯಕಾಂತಿ",
    "chilli": "ಮೆಣಸಿನಕಾಯಿ",
    # Newly added
    "tomato": "ಟೊಮ್ಯಾಟೊ",
    "potato": "ಆಲೂಗಡ್ಡೆ",
    "onion": "ಈರುಳ್ಳಿ",
    "pomegranate": "ದಾಳಿಂಬೆ",
    "mango": "ಮಾವು",
    "grapes": "ದ್ರಾಕ್ಷಿ",
    "black gram": "ಉದ್ದಿನಬೇಳೆ",
    "green gram": "ಹೇಶರು",
    "pigeon pea": "ತೊಗರಿ",
}


def enrich_existing_crop(base_result: dict, lang: str, fallback_crop: str):
    # Always ensure cropName exists
    crop_name = base_result.get("cropName") or fallback_crop
    crop_eng = crop_name.lower().strip()

    base_result["cropName"] = crop_name

    # 💰 Market price
    price = market_price_ktk.get(crop_eng)
    base_result["marketPrice"] = (
        f"₹ {price} /quintal" if price else "Market data unavailable"
    )

    # 📈 Profit
    if price and crop_eng in cultivation_cost and crop_eng in yield_per_acre:
        net = (price * yield_per_acre[crop_eng]) - cultivation_cost[crop_eng]
        base_result["estimatedNetProfitPerAcre"] = f"₹ {net} /acre"
    else:
        base_result["estimatedNetProfitPerAcre"] = "Profit data unavailable"

    

    return base_result



# ============ KNOWLEDGE BASE FOR KARNATAKA =================
locality_crops = {
    "uttara kannada": ["areca nut", "pepper", "paddy","rice", "banana", "turmeric"],
    "belagavi": ["sugarcane", "soybean", "maize", "paddy","rice", "wheat"],
    "shivamogga": ["areca nut", "pepper", "paddy","rice", "banana", "ginger"],
    "dharwad": ["soybean", "cotton", "maize", "groundnut", "rice","sunflower"],
    "haveri": ["cotton", "chilli", "maize", "paddy","rice", "jowar"],
    "ballari": ["pomegranate", "groundnut", "sunflower""rice", "cotton"],
    "chikkamagaluru": ["coffee", "pepper", "areca nut","rice", "banana"],
    "mysuru": ["cotton", "ragi", "paddy", "groundnut","rice", "sugarcane"],
    "mandya": ["sugarcane", "paddy", "mulberry","rice", "banana"],
    "tumakuru": ["ragi", "groundnut", "pigeon pea", "rice","tomato"],
}

soil_crops = {
    "red soil": ["areca nut", "pepper", "cotton", "groundnut", "ragi", "paddy","rice"],
    "black soil": ["cotton", "soybean", "turmeric", "paddy", "rice","banana"],
    "laterite": ["areca nut", "pepper", "coffee", "banana"],
    "alluvial": ["paddy","rice", "sugarcane", "banana", "vegetables"],
    "sandy": ["groundnut", "onion", "melon", "cucumber"],
}

temp_range = {
    "areca nut": (18, 32), "pepper": (20, 30), "coffee": (15, 28),
    "banana": (15, 35), "cotton": (22, 32), "soybean": (20, 32),
    "maize": (20, 32), "paddy": (18, 38), "groundnut": (20, 36),
    "turmeric": (20, 30), "sugarcane": (20, 35),"rice": (18, 38),
}

rainfall_range = {
    "areca nut": (2000, 3500), "pepper": (2000, 3000), "coffee": (1800, 3000),
    "paddy": (900, 2500), "cotton": (600, 1200), "soybean": (700, 1200),
    "maize": (500, 900), "groundnut": (500, 1200), "banana": (1100, 3000),
    "turmeric": (900, 1800), "sugarcane": (1100, 2200),"rice": (900, 2500),
}






# ================ EXISTING CROP ADVICE =================
# ======================================================

# --------------------------------------------------
# EXISTING CROP API
# --------------------------------------------------
@app.post("/advice/existing/full", response_model=ExistingCropFullResponse)
def existing_crop_advice(req: ExistingCropRequest):

    # ---------- PRIMARY ----------
    primary_crop_name = extract_crop_name(req.activityLogs)
    primary_result = existing_crop_advisor.advise(
        req.activityLogs,
        primary_crop_name
    )
    primary_resp = ExistingCropResponse(**primary_result)

    # ---------- SECONDARY ----------
    secondary_responses = []

    for sc in req.secondaryCrops:
        sc_name = extract_crop_name(sc.activityLogs, sc.cropName)
        sc_result = existing_crop_advisor.advise(
            sc.activityLogs,
            sc_name
        )
        secondary_responses.append(
            ExistingCropResponse(**sc_result)
        )

    return ExistingCropFullResponse(
        primaryCropAdvice=primary_resp,
        secondaryCropsAdvice=secondary_responses
    )
@app.post("/advice/existing/full", response_model=ExistingCropFullResponse)
def existing_crop_advice(req: ExistingCropRequest):

    # PRIMARY
    primary_advice = generate_advice(req.activityLogs)

    # SECONDARY
    secondary = []
    for sc in req.secondaryCrops:
        adv = generate_advice(sc.activityLogs)
        adv["cropName"] = sc.cropName.title()
        secondary.append(adv)

    return {
        "primaryCropAdvice": primary_advice,
        "secondaryCropsAdvice": secondary
    }       

# ================ NEW CROP ADVICE =================
@app.post("/advice/new", response_model=NewCropResponse)
def new_crop_advice(req: NewCropRequest):
    try:
        
        payload = req.dict()
        base_recs = new_crop_advisor.recommend(payload, top_k=6)

        lang = (req.language or "en").lower()
        district = (req.district or "").lower()
        soil = (req.soilType or "").lower()
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
            

            # ⭐ MARKET PRICE
            price = market_price_ktk.get(crop)
            r["avgMarketPricePerQuintal"] = price if price else None


             # ⭐ PROFIT ESTIMATION
            if price and crop in yield_per_acre and crop in cultivation_cost:
                expected_yield = yield_per_acre[crop]
                net_profit = (price * expected_yield) - cultivation_cost[crop]

                r["expectedYieldPerAcreQuintal"] = expected_yield
                r["estimatedNetProfitPerAcre"] = int(net_profit)
            else:
                r["expectedYieldPerAcreQuintal"] = None
                r["estimatedNetProfitPerAcre"] = None

            # ⭐ Price source tag
            r["priceSource"] = "Based on 2025 Karnataka Mandi Avg"

            ranked.append(r)


        ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)[:4]

        # language switch
        if lang != "en":
            for r in ranked:
                crop_lower = r["cropName"].lower()
                r["cropName"] = CROP_NAME_KN.get(crop_lower, r["cropName"])
                for key in ("waterManagement", "nutrientManagement",
                            "seedSelection", "otherAdvice"):
                    try:
                        r[key] = translate_text(r[key], lang)
                    except Exception:
                        pass

        return {"recommendations": ranked}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ================ PEST DETECTION LOGIC =================

# ---- PEST RISK API ----
@app.post("/pest/risk", response_model=PestRiskResponse)
def pest_risk(req: PestRiskRequest):

    user_ref = firebase_db.reference(f"Users/{req.userId}")
    user = user_ref.get()

    if not user:
        return {"alerts": []}

    farm = user.get("farmDetails", {})
    district = farm.get("district")
    soil = farm.get("soilType")

    alerts = []

    # -------- PRIMARY CROP --------
    primary_crop = farm.get("cropName")
    if primary_crop:
        results = engine.predict(
            cropName=primary_crop,
            district=district,
            soilType=soil,
            month=datetime.now().month
        )
        alerts.extend(results)

    # -------- SECONDARY CROPS --------
    for crop_name in user.get("secondaryCrops", {}).keys():
        results = engine.predict(
            cropName=crop_name,
            district=district,
            soilType=soil,
            month=datetime.now().month
        )
        alerts.extend(results)

    return {"alerts": alerts}

# =====================================================
# ✅ HEALTH CHECK
# =====================================================

@app.get("/")
def root():
    return {"status": "running", "message": "Crop advisory backend active"}

 










































