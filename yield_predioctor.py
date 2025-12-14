# yield_predictor.py

from typing import Dict

class YieldPredictor:
    """
    Knowledge-based yield prediction for Karnataka crops.
    Uses average yield + weather adjustments.
    """

    # 🌾 Average Yield (Quintals per Acre) — Karnataka
    CROP_YIELD_BASE: Dict[str, float] = {
        # Cereals
        "rice": 22,
        "paddy": 22,
        "maize": 18,
        "ragi": 10,
        "wheat": 16,
        "jowar": 12,

        # Pulses
        "green gram": 5,
        "black gram": 5,
        "pigeon pea": 6,
        "chickpea": 7,

        # Oilseeds
        "groundnut": 9,
        "soybean": 7,
        "sunflower": 6,

        # Commercial crops
        "cotton": 5,
        "sugarcane": 40,

        # Plantation & spices
        "areca nut": 10,
        "coffee": 7,
        "pepper": 3,
        "turmeric": 55,
        "ginger": 65,

        # Horticulture
        "banana": 35,
        "mango": 55,
        "grapes": 60,
        "pomegranate": 30,
        "tomato": 100,
        "potato": 75,
        "onion": 80,
        "chilli": 30,
    }

    def predict(self, crop: str, rainfall: float, temp: float, farm_size: float):

        crop_key = crop.lower().strip()

        # 🌱 Base yield from KB
        base_yield = self.CROP_YIELD_BASE.get(crop_key, 12.0)

        explanation = [
            f"Average yield for {crop} in Karnataka is about {base_yield} quintals per acre."
        ]

        # 🌧 Rainfall adjustment
        if rainfall > 2500:
            base_yield *= 1.08
            explanation.append("Good monsoon rainfall is expected to improve yield.")
        elif rainfall < 800:
            base_yield *= 0.85
            explanation.append("Low rainfall may reduce crop productivity.")
        else:
            explanation.append("Rainfall conditions are within optimal range.")

        # 🌡 Temperature adjustment
        if temp > 35:
            base_yield *= 0.9
            explanation.append("High temperatures may stress the crop.")
        elif temp < 18:
            base_yield *= 0.92
            explanation.append("Low temperature may slow crop growth.")
        else:
            explanation.append("Temperature conditions are favorable.")

        expected_per_acre = round(base_yield, 2)
        total_yield = round(expected_per_acre * farm_size, 2)

        # 🎯 Confidence estimation
        if rainfall >= 1000 and 20 <= temp <= 32:
            confidence = "High"
        elif rainfall >= 700:
            confidence = "Medium"
        else:
            confidence = "Low"

        return {
            "expectedYieldPerAcre": expected_per_acre,
            "totalExpectedYield": total_yield,
            "confidence": confidence,
            "explanation": " ".join(explanation)
        }
