
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




app = FastAPI(title="Crop Advisory Backend")

new_crop_advisor = NewCropAdvisor()
existing_crop_advisor = ExistingCropAdvisor()
engine = PestEngine(PEST_DB, PEST_HISTORY)

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
    farmDetails: FarmDetails
    activityLogs: List[Dict] = []          # primary crop logs
    secondaryCrops: List[SecondaryCropModel] = []
    language: Optional[str] = "en"


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


class CropLogBlock(BaseModel):
    cropName: str
    stage: Optional[str] = None
    activityLogs: Optional[List[dict]] = []
    
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

class CropRisk(BaseModel):
    cropName: str
    stage: Optional[str]

class PestRiskResponse(BaseModel):
    alerts: List[PestAlert]
    
def get_user_crops(db, user_id: str):
    crops = {}
    logs = db.child("Users").child(user_id).child("farmActivityLogs").get() or {}

    for crop_key, activities in logs.items():
        for _, act in activities.items():
            name = act.get("cropName")
            stage = act.get("stage")
            if name:
                crops[name.lower()] = stage

    return [
        {"cropName": k, "stage": v}
        for k, v in crops.items()
    ]


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

class ExistingCropAdvisor:

    def advise(self, logs, crop_name: str | None):

        crop = crop_name or "Unknown Crop"

        if not logs:
            return {
                "cropName": crop,
                "cropManagement": ["No activity logs found yet. Please add farm activities."],
                "nutrientManagement": [],
                "waterManagement": [],
                "protectionManagement": [],
                "harvestMarketing": []
            }

        rec = {
            "cropManagement": [],
            "nutrientManagement": [],
            "waterManagement": [],
            "protectionManagement": [],
            "harvestMarketing": []
        }

        for log in logs:
            sub = (log.get("subActivity") or "").lower()

            if sub == "soil_preparation":
                rec["cropManagement"].append(
                    "Soil preparation completed. Ensure proper leveling and drainage."
                )

            elif sub == "sowing_planting":
                rec["cropManagement"].append(
                    "Crop planted successfully. Maintain recommended spacing."
                )

            elif sub == "nutrient_management":
                rec["nutrientManagement"].append(
                    "Apply fertilizers in split doses as per crop stage."
                )

            elif sub == "water_management":
                rec["waterManagement"].append(
                    "Maintain optimal soil moisture. Avoid water stress."
                )

            elif sub == "crop_protection_maintenance":
                rec["protectionManagement"].append(
                    "Monitor pests weekly and apply control measures if needed."
                )

            elif sub == "harvesting_cut_gather":
                rec["harvestMarketing"].append(
                    "Harvest at proper maturity and store in dry conditions."
                )

        # Final safety fallback
        for k in rec:
            if not rec[k]:
                rec[k].append("Follow recommended best practices for this crop.")

        return {
            "cropName": crop,
            **rec
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

    # 🌐 Language translation (optional)
    if lang != "en":
        base_result["cropName"] = CROP_NAME_KN.get(crop_eng, crop_name)

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




score = 0.0

if stage in pest["stage"]:
    score += 0.4

if district in PEST_HISTORY.get(crop, []):
    score += 0.3

if temp >= rule["temp_range"][0] and temp <= rule["temp_range"][1] \
        and humidity >= rule.get("humidity_gt", 0):
    score += 0.2


riskLevel = (
    "High" if score >= 0.7
    else "Medium" if score >= 0.4
    else "Low"
)

# ================ EXISTING CROP ADVICE =================
# ======================================================

@app.post("/advice/existing/full", response_model=ExistingCropFullResponse)
def existing_crop_advice(req: ExistingCropRequest):

    advisor = ExistingCropAdvisor()

    # ---------- PRIMARY CROP ----------
    primary_crop = req.farmDetails.cropName or "Primary Crop"

    primary_advice = advisor.advise(
        req.activityLogs,
        primary_crop
    )

    # ---------- SECONDARY CROPS ----------
    secondary_results = []
    for sc in req.secondaryCrops:
        sc_advice = advisor.advise(
            sc.activityLogs,
            sc.cropName
        )
        secondary_results.append(
            ExistingCropResponse(**sc_advice)
        )

    return ExistingCropFullResponse(
        primaryCropAdvice=ExistingCropResponse(**primary_advice),
        secondaryCropsAdvice=secondary_results
    )
        

       

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

@app.post("/pest/risk", response_model=PestRiskResponse)
def pest_risk(req: PestRiskRequest):

    crops = get_user_crops(firebase_db, req.userId)

    if not crops:
        return {"alerts": []}

    alerts = []

    for crop in crops:
        results = engine.predict(
            cropName=crop["cropName"],
            stage=crop["stage"],
            district=None,      # can be enhanced later
            soilType=None,
            temp=None,
            humidity=None,
            month_int=datetime.now().month
        )

        for r in results:
            alerts.append({
                "cropName": crop["cropName"],
                "pestName": r["pestName"],
                "riskLevel": r["riskLevel"],
                "score": r["score"],
                "reasons": r["reasons"],
                "symptoms": r["symptoms"],
                "preventive": r["preventive"],
                "corrective": r["corrective"]
            })

    return {"alerts": alerts}

@app.get("/")
def root():
    return {"status": "running", "message": "Crop advisory backend active"}

 






























