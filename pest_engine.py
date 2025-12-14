# pest_engine.py
from datetime import datetime
from typing import List, Dict


class PestEngine:

    def __init__(self, pest_db: Dict, district_history: Dict, firebase_db):
        self.pest_db = pest_db
        self.district_history = district_history
        self.firebase_db = firebase_db

    # --------------------------------------------------
    # Fetch crops (PRIMARY + SECONDARY) from Firebase
    # --------------------------------------------------
    def get_user_crops(self, user_id: str):
        ref = self.firebase_db.reference(f"Users/{user_id}")
        user = ref.get()

        if not user:
            return []

        crops = []

        # PRIMARY CROP
        farm = user.get("farmDetails", {})
        primary_crop = farm.get("cropName")
        district = farm.get("district", "").lower()
        soil = farm.get("soilType", "").lower()

        if primary_crop:
            crops.append({
                "cropName": primary_crop.lower(),
                "district": district,
                "soil": soil
            })

        # SECONDARY CROPS
        secondary = user.get("secondaryCrops", {})
        for crop_name in secondary.keys():
            crops.append({
                "cropName": crop_name.lower(),
                "district": district,
                "soil": soil
            })

        return crops

    # --------------------------------------------------
    # Core pest detection logic
    # --------------------------------------------------
    def detect_pests(self, user_id: str):
        crops = self.get_user_crops(user_id)
        alerts = []

        month = datetime.now().strftime("%B")

        for crop in crops:
            crop_name = crop["cropName"]
            district = crop["district"]

            if crop_name not in self.pest_db:
                continue

            for pest_name, rule in self.pest_db[crop_name].items():
                score = 0
                reasons = []

                # 🌦 Season check
                if month in rule.get("season", []):
                    score += 0.4
                    reasons.append(f"Seasonal occurrence in {month}")

                # 📍 District history boost
                hist = self.district_history.get(district, {}).get(crop_name, {})
                if pest_name in hist:
                    score += 0.4
                    reasons.append("Previously reported in your district")

                # 🎯 Risk threshold
                if score >= 0.4:
                    risk = "HIGH" if score >= 0.75 else "MEDIUM"

                    alerts.append({
                        "cropName": crop_name.title(),
                        "pestName": pest_name,
                        "riskLevel": risk,
                        "score": round(score, 2),
                        "reasons": reasons,
                        "symptoms": rule.get("symptoms", ""),
                        "preventive": rule.get("preventive", ""),
                        "corrective": rule.get("corrective", "")
                    })

        return alerts
