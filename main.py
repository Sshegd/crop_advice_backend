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
    avgMarketPricePerQuintal: Optional[int] = None
    expectedYieldPerAcreQuintal: Optional[int] = None
    estimatedNetProfitPerAcre: Optional[int] = None
    priceSource: Optional[str] = None


class NewCropResponse(BaseModel):
    recommendations: List[NewCropAdvice]

# ====== MARKET PRICE (KARNATAKA MANDI AVERAGE ₹/QUINTAL) ======
# ====== MARKET PRICE (Karnataka Avg ₹/Quintal 2024–25) ======
market_price_ktk = {
    "areca nut": 58000,
    "pepper": 64000,
    "paddy": 3300,
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

def normalize_language(lang: str):
    if not lang:
        return "en"
    lang = lang.strip().lower()
    if lang in ["kn", "kan", "kannada", "kn-in", "ಕನ್ನಡ"]:
        return "kn"
    return "en"
# ================ EXISTING CROP ADVICE =================
# ================ EXISTING CROP ADVICE =================
@app.post("/advice/existing", response_model=ExistingCropResponse)
def existing_crop_advice(req: ExistingCropRequest):
    try:
        # Generate advisory from logs using ML / rule engine
        result = existing_crop_advisor.advise(req.activityLogs, req.farmDetails.dict())
        lang = normalize_language(req.language)
        crop_eng = result["cropName"].lower()


        # ⭐ MARKET PRICE
        price = market_price_ktk.get(crop_eng)
        if price:
            result["marketPrice"] = f"₹ {price} /quintal"
        else:
            result["marketPrice"] = "Market data unavailable"

        # ⭐ PROFIT ESTIMATION
        if price and crop_eng in cultivation_cost and crop_eng in yield_per_acre:
            expected_yield = yield_per_acre[crop_eng]
            net_profit = (price * expected_yield) - cultivation_cost[crop_eng]
            result["estimatedNetProfitPerAcre"] = f"₹ {net_profit} /acre"
        else:
            result["estimatedNetProfitPerAcre"] = "Profit calculation unavailable"

        # Translation
        if lang == "kn":
            result["cropName"] = CROP_NAME_KN.get(crop_eng, result["cropName"])

            for key in ["cropManagement", "nutrientManagement", "waterManagement",
                        "protectionManagement", "harvestMarketing"]:
                result[key] = [
                    translate_text(item, target_language="kn") for item in result[key]
                ]

            # Translate meta-text also
            result["marketPrice"] = translate_text(result["marketPrice"], target_language="kn")
            result["estimatedNetProfitPerAcre"] = translate_text(result["estimatedNetProfitPerAcre"], target_language="kn")

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# ================ NEW CROP ADVICE =================
@app.post("/advice/new", response_model=NewCropResponse)
def new_crop_advice(req: NewCropRequest):
    try:
        lang = normalize_language(req.language)
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

         # Translation
        if lang == "kn":
            for r in ranked:
                crop = r["cropName"].lower()
                r["cropName"] = CROP_NAME_KN.get(crop, r["cropName"])
                for key in ["waterManagement", "nutrientManagement", "seedSelection", "otherAdvice"]:
                    r[key] = translate_text(r[key], target_language="kn")

        return {"recommendations": ranked}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"status": "running", "message": "Crop advisory backend active"}
 










