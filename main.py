from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Optional
from ml_advisor import NewCropAdvisor, ExistingCropAdvisor
from google_translate import translate_text
from datetime import datetime
from pest_db import PEST_DB


app = FastAPI(title="Crop Advisory Backend")

new_crop_advisor = NewCropAdvisor()
existing_crop_advisor = ExistingCropAdvisor()


# ============================================================
# MODELS
# ============================================================

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
    marketPrice: Optional[str] = None
    estimatedNetProfitPerAcre: Optional[str] = None


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


# ============================================================
# PEST DETECTION MODELS
# ============================================================

class PestDetectionRequest(BaseModel):
    cropName: str
    district: Optional[str] = None
    taluk: Optional[str] = None
    stage: Optional[str] = None
    avgTemp: Optional[float] = None
    humidity: Optional[float] = None
    rainfall: Optional[float] = None
    month: Optional[int] = None
    symptomsText: Optional[str] = None
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


class PestResponse(BaseModel):
    alerts: List[PestAlert]


# ============================================================
# STATIC DATA (Prices, cultivation cost, yields…)
# ============================================================

market_price_ktk = {
    "areca nut": 58000,
    "pepper": 64000,
    "paddy": 3300,
    "rice": 3300,
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

cultivation_cost = {
    "areca nut": 60000,
    "pepper": 50000,
    "paddy": 38000,
    "rice": 38000,
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

yield_per_acre = {
    "areca nut": 10, "pepper": 3, "paddy": 22, "rice": 22, "sugarcane": 40,
    "maize": 18, "banana": 35, "ginger": 65, "turmeric": 55, "soybean": 7,
    "cotton": 5, "groundnut": 9, "ragi": 10, "coffee": 7, "sunflower": 6,
    "chilli": 30, "tomato": 100, "potato": 75, "onion": 80, "pomegranate": 30,
    "mango": 55, "grapes": 60, "black gram": 5, "green gram": 5, "pigeon pea": 6
}

CROP_NAME_KN = {
    "areca nut": "ಅಡಿಕೆ",
    "banana": "ಬಾಳೆ",
    "paddy": "ಅಕ್ಕಿ",
    "rice": "ಅಕ್ಕಿ",
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

# (locality_crops, soil_crops, temp_range, rainfall_range remain same)


# ============================================================
# EXISTING CROP ADVICE
# ============================================================

@app.post("/advice/existing", response_model=ExistingCropResponse)
def existing_crop_advice(req: ExistingCropRequest):
    try:
        result = existing_crop_advisor.advise(req.activityLogs, req.farmDetails.dict())
        lang = req.language.lower()
        crop_eng = result["cropName"].lower()

        price = market_price_ktk.get(crop_eng)
        if price:
            result["marketPrice"] = f"₹ {price} /quintal"

        if price and crop_eng in cultivation_cost and crop_eng in yield_per_acre:
            expected_yield = yield_per_acre[crop_eng]
            net_profit = (price * expected_yield) - cultivation_cost[crop_eng]
            result["estimatedNetProfitPerAcre"] = f"₹ {net_profit}"

        if lang != "en":
            result["cropName"] = CROP_NAME_KN.get(crop_eng, result["cropName"])
            for key in [
                "cropManagement", "nutrientManagement", "waterManagement",
                "protectionManagement", "harvestMarketing"
            ]:
                result[key] = [translate_text(s, lang) for s in result[key]]

            for meta in ["marketPrice", "estimatedNetProfitPerAcre"]:
                result[meta] = translate_text(result[meta], lang)

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# NEW CROP ADVICE
# ============================================================

@app.post("/advice/new", response_model=NewCropResponse)
def new_crop_advice(req: NewCropRequest):
    try:
        payload = req.dict()
        base_recs = new_crop_advisor.recommend(payload, top_k=6)

        lang = req.language.lower()
        district = req.district.lower()
        soil = req.soilType.lower()

        rain, temp = req.avgRainfall, req.avgTemp

        ranked = []
        for r in base_recs:
            crop = r["cropName"].lower()
            score = r["score"]

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

            price = market_price_ktk.get(crop)
            r["avgMarketPricePerQuintal"] = price

            if price and crop in yield_per_acre and crop in cultivation_cost:
                expected_yield = yield_per_acre[crop]
                r["expectedYieldPerAcreQuintal"] = expected_yield
                r["estimatedNetProfitPerAcre"] = (price * expected_yield) - cultivation_cost[crop]

            r["score"] = round(score, 3)
            r["priceSource"] = "Based on 2025 Karnataka Mandi Avg"

            ranked.append(r)

        ranked = sorted(ranked, key=lambda x: x["score"], reverse=True)[:4]

        if lang != "en":
            for r in ranked:
                crop_lower = r["cropName"].lower()
                r["cropName"] = CROP_NAME_KN.get(crop_lower, r["cropName"])
                for key in ["waterManagement", "nutrientManagement", "seedSelection", "otherAdvice"]:
                    r[key] = translate_text(r[key], lang)

        return {"recommendations": ranked}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# PEST DETECTION ENGINE
# ============================================================

def _month_name(month_int: Optional[int]) -> str:
    if month_int is None:
        month_int = datetime.utcnow().month
    return datetime(2000, month_int, 1).strftime("%B")


def _evaluate_single_rule(rule, stage, temp, hum, rain, month_name, symptoms_text):
    reasons = []
    total_cond = 0
    matched = 0

    if "temp_gt" in rule and temp:
        total_cond += 1
        if temp > rule["temp_gt"]:
            matched += 1
            reasons.append(f"Temperature {temp}°C > {rule['temp_gt']}°C")

    if "temp_range" in rule and temp:
        total_cond += 1
        lo, hi = rule["temp_range"]
        if lo <= temp <= hi:
            matched += 1
            reasons.append(f"Temperature {temp}°C within {lo}-{hi}°C")

    if "humidity_gt" in rule and hum:
        total_cond += 1
        if hum > rule["humidity_gt"]:
            matched += 1
            reasons.append(f"Humidity > {rule['humidity_gt']}%")

    if "humidity_lt" in rule and hum:
        total_cond += 1
        if hum < rule["humidity_lt"]:
            matched += 1
            reasons.append(f"Humidity < {rule['humidity_lt']}%")

    if "rainfall_gt" in rule and rain:
        total_cond += 1
        if rain > rule["rainfall_gt"]:
            matched += 1
            reasons.append(f"Rainfall > {rule['rainfall_gt']}mm")

    if "rainfall_lt" in rule and rain:
        total_cond += 1
        if rain < rule["rainfall_lt"]:
            matched += 1
            reasons.append(f"Rainfall < {rule['rainfall_lt']}mm")

    if "season" in rule:
        total_cond += 1
        if month_name in rule["season"]:
            matched += 1
            reasons.append(f"Season: {month_name}")

    if "stage" in rule and stage:
        total_cond += 1
        if stage in rule["stage"]:
            matched += 1
            reasons.append(f"Stage risk: {stage}")

    score = matched / total_cond if total_cond > 0 else 0

    if symptoms_text:
        if any(w in symptoms_text.lower() for w in rule.get("symptoms", "").lower().split()):
            score = min(1.0, score + 0.15)
            reasons.append("Farmer symptoms match observed patterns")

    return score, reasons


def _risk_level(score):
    if score >= 0.75:
        return "HIGH"
    if score >= 0.45:
        return "MEDIUM"
    return "LOW"


@app.post("/pest/detect", response_model=PestResponse)
def detect_pest(req: PestDetectionRequest):
    try:
        crop = req.cropName.lower()
        if crop not in PEST_DB:
            raise HTTPException(404, f"No pest data for {req.cropName}")

        month_name = _month_name(req.month)

        alerts = []

        for pest_name, rule in PEST_DB[crop].items():
            score, reasons = _evaluate_single_rule(
                rule,
                req.stage,
                req.avgTemp,
                req.humidity,
                req.rainfall,
                month_name,
                req.symptomsText,
            )

            if score < 0.45:
                continue

            symptoms = rule.get("symptoms", "")
            preventive = rule.get("preventive", "")
            corrective = rule.get("corrective", "")

            if req.language != "en":
                try:
                    pest_name = translate_text(pest_name, req.language)
                    symptoms = translate_text(symptoms, req.language)
                    preventive = translate_text(preventive, req.language)
                    corrective = translate_text(corrective, req.language)
                except:
                    pass

            alerts.append(
                PestAlert(
                    cropName=req.cropName if req.language == "en" else CROP_NAME_KN.get(crop, req.cropName),
                    pestName=pest_name,
                    riskLevel=_risk_level(score),
                    score=round(score, 2),
                    reasons=reasons,
                    symptoms=symptoms,
                    preventive=preventive,
                    corrective=corrective,
                )
            )

        return PestResponse(alerts=alerts)

    except Exception as e:
        raise HTTPException(500, str(e))



@app.get("/")
def root():
    return {"status": "running", "message": "Crop advisory backend active"}
