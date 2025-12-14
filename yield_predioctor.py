# yield_predictor.py
from typing import Dict

# Base yield per acre (Karnataka avg – quintals/acre)
BASE_YIELD = {
    "areca nut": 12,
    "chilli": 30,
    "paddy": 22,
    "rice": 22,
    "banana": 35,
    "maize": 18,
    "ragi": 10,
}

class YieldPredictor:

    def predict(self, crop: str, rainfall: float, temp: float, farm_size: float) -> Dict:
        crop_key = crop.lower().strip()
        base = BASE_YIELD.get(crop_key, 20)

        # 🌧 Rainfall factor
        if rainfall < 700:
            factor = 0.8
        elif rainfall > 2000:
            factor = 0.9
        else:
            factor = 1.0

        # 🌡 Temperature factor
        if temp < 15 or temp > 38:
            factor *= 0.85

        expected_per_acre = round(base * factor, 2)
        total = round(expected_per_acre * farm_size, 2)

        confidence = "High" if factor >= 1 else "Medium"

        return {
            "expectedYieldPerAcre": expected_per_acre,
            "totalExpectedYield": total,
            "confidence": confidence,
            "explanation": (
                f"Based on recent weather patterns and historical data, "
                f"{crop} is expected to yield approximately "
                f"{expected_per_acre} quintals per acre."
            )
        }
