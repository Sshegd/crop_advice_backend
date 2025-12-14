from collections import Counter
from datetime import datetime

def extract_features(logs: list, crop_name: str):

    features = {
        "crop": crop_name.lower(),
        "activity_count": len(logs),
        "soil_preparation": 0,
        "sowing": 0,
        "nutrient": 0,
        "water": 0,
        "protection": 0,
        "harvest": 0,
    }

    for log in logs:
        sub = (log.get("subActivity") or "").lower()

        if "soil" in sub:
            features["soil_preparation"] += 1
        elif "sowing" in sub:
            features["sowing"] += 1
        elif "nutrient" in sub:
            features["nutrient"] += 1
        elif "water" in sub:
            features["water"] += 1
        elif "protection" in sub:
            features["protection"] += 1
        elif "harvest" in sub:
            features["harvest"] += 1

    return features
