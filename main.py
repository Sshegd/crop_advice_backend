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
    estimatedNetProfitPerAcre: Optional[int] = None


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
            for key, val in result.items():
                if isinstance(val, list):
                    translated_items = []
                    for sentence in val:
                        try:
                            translated_items.append(translate_text(sentence, target_language=lang))
                        except:
                            translated_items.append(sentence)
                    result[key] = translated_items

            # Translate crop name using dictionary
            crop_lower = result["cropName"].lower()
            result["cropName"] = CROP_NAME_KN.get(crop_lower, result["cropName"])

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ====== MARKET PRICE (KARNATAKA MANDI AVERAGE ₹/QUINTAL) ======
market_price_ktk = {
    "areca nut": 54000,
    "pepper": 62000,
    "paddy": 3200,
    "sugarcane": 3500,
    "maize": 2200,
    "banana": 1600,
    "ginger": 8200,
    "turmeric": 7200,
    "soybean": 4600,
    "cotton": 6200,
    "groundnut": 6200,
    "ragi": 3200,
    "coffee": 23000,
    "sunflower": 6100,
    "chilli": 11000,
}
# ====== COST OF CULTIVATION PER ACRE (Approx based on Karnataka agriculture dept) ======
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
}
# ====== YIELD PER ACRE (quintals) ======
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
}
# English → Kannada crop names
CROP_NAME_KN = {
    "areca nut": "ಅಡಿಕೆ",
    "banana": "ಬಾಳೆ",
    "paddy": "ಅಕ್ಕಿ",
    "pepper": "ಮೆಣಸು",
    "turmeric": "ಅರಿಶಿನ",
    "ginger": "ಶುಂಠಿ",
    "sugarcane": "ಕರಿಬೇವು",
    "groundnut": "ಶೇಂಗಾ",
    "maize": "ಮೆಕ್ಕೆಜೋಳ",
    "ragi": "ರಾಗಿ",
    "cotton": "ಹತ್ತಿ",
    "soybean": "ಸೋಯಾಬೀನ್",
    "coffee": "ಕಾಫಿ",
    "sunflower": "ಸೂರ್ಯಕಾಂತಿ",
    "chilli": "ಮೆಣಸಿನಕಾಯಿ",
}


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

        if req.language.lower() != "en":
           for r in ranked:
                # Translate crop name using dictionary (not API)
                crop_lower = r["cropName"].lower()
                r["cropName"] = CROP_NAME_KN.get(crop_lower, r["cropName"])

                # Translate all advisory sentences safely
                if lang != "en":
                    for key in ("waterManagement", "nutrientManagement", "seedSelection", "otherAdvice"):
                        try:
                            r[key] = translate_text(r[key], target_language=lang)
                        except:
                            pass  # fallback if translation fails

            return {"recommendations": ranked[:4]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/")
def root():
    return {"status": "running", "message": "Crop advisory backend active"}
 




