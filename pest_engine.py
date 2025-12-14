# pest_engine.py
from datetime import datetime


class PestEngine:

    def __init__(self, pest_db, pest_history, firebase_db):
        self.pest_db = pest_db
        self.pest_history = pest_history
        self.db = firebase_db

    # -------------------------------------------------
    def _risk_label(self, score):
        if score >= 0.75:
            return "HIGH"
        if score >= 0.4:
            return "MEDIUM"
        return "LOW"

    # -------------------------------------------------
    def predict_for_user(self, user_id: str, month_int: int, lang="en"):
        """
        MAIN ENTRY POINT
        """
        ref = self.db.reference(f"Users/{user_id}")
        user = ref.get()

        if not user:
            return []

        farm = user.get("farmDetails", {})
        district = (farm.get("district") or "").lower()
        soil = (farm.get("soilType") or "").lower()

        alerts = []

        # ---------- PRIMARY CROP ----------
        primary_crop = (farm.get("cropName") or "").lower()
        if primary_crop:
            alerts.extend(
                self._predict_for_crop(primary_crop, district, soil, month_int)
            )

        # ---------- SECONDARY CROPS ----------
        for crop_name in user.get("secondaryCrops", {}).keys():
            alerts.extend(
                self._predict_for_crop(crop_name.lower(), district, soil, month_int)
            )

        return alerts

    # -------------------------------------------------
    def _predict_for_crop(self, crop, district, soil, month_int):
        results = []

        month_name = datetime(2000, month_int, 1).strftime("%B")

        # ---------- DISTRICT HISTORY ----------
        district_pests = (
            self.pest_history
                .get(district, {})
                .get(crop, {})
        )

        # ---------- PEST DB ----------
        crop_pests = self.pest_db.get(crop, {})

        for pest_name, rule in crop_pests.items():

            score = 0.3   # BASE SCORE (IMPORTANT)
            reasons = []

            # District history boost (MOST IMPORTANT)
            if pest_name in district_pests:
                score += 0.4
                reasons.append("Reported frequently in this district")

            # Seasonal match
            if month_name in rule.get("season", []):
                score += 0.2
                reasons.append(f"Seasonal risk during {month_name}")

            # Soil match
            if soil and soil in [s.lower() for s in rule.get("soil", [])]:
                score += 0.1
                reasons.append(f"Soil type ({soil}) favors pest")

            score = min(score, 1.0)

            results.append({
                "cropName": crop.title(),
                "pestName": pest_name,
                "riskLevel": self._risk_label(score),
                "score": round(score, 2),
                "reasons": reasons,
                "symptoms": rule.get("symptoms", ""),
                "preventive": rule.get("preventive", ""),
                "corrective": rule.get("corrective", "")
            })

        return results
