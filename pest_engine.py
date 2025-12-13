# pest_engine.py
from typing import Dict, Optional
from datetime import datetime


class PestEngine:

    def __init__(self, pest_db: Dict, pest_history: Dict):
        self.pest_db = pest_db
        self.pest_history = pest_history

    # -----------------------------
    # HELPERS
    # -----------------------------
    def _month_name(self, month_int: Optional[int]) -> str:
        if not month_int:
            month_int = datetime.utcnow().month
        return datetime(2000, month_int, 1).strftime("%B")

    def _risk_level(self, score: float) -> str:
        if score >= 0.7:
            return "HIGH"
        if score >= 0.4:
            return "MEDIUM"
        return "LOW"

    def _history_score(self, level: Optional[str]) -> float:
        return {
            "HIGH": 0.6,
            "MEDIUM": 0.4,
            "LOW": 0.2
        }.get(level, 0.0)

    # -----------------------------
    # MAIN ENGINE
    # -----------------------------
    def predict(
        self,
        cropName: str,
        district: str = None,
        soilType: str = None,
        stage: str = None,
        temp: float = None,
        humidity: float = None,
        rainfall: float = None,
        month_int: int = None,
        lang: str = "en"
    ):

        if not cropName:
            return []

        crop = cropName.lower().strip()
        district = (district or "").lower().strip()
        soilType = (soilType or "").lower().strip()
        stage = (stage or "").lower().strip()

        # SAFE DEFAULTS (CRITICAL)
        temp = temp if temp is not None else 28
        humidity = humidity if humidity is not None else 70
        rainfall = rainfall if rainfall is not None else 900

        month_name = self._month_name(month_int)

        if crop not in self.pest_db:
            return []

        alerts = []

        for pest_name, rule in self.pest_db[crop].items():

            score = 0.3   # ⭐ BASE RISK (VERY IMPORTANT)
            reasons = ["General pest risk for this crop"]

            # TEMP
            if "temp_range" in rule:
                lo, hi = rule["temp_range"]
                if lo <= temp <= hi:
                    score += 0.15
                    reasons.append(f"Temperature favorable ({temp}°C)")

            # HUMIDITY
            if "humidity_gt" in rule and humidity >= rule["humidity_gt"]:
                score += 0.15
                reasons.append(f"High humidity ({humidity}%)")

            # RAINFALL
            if "rainfall_range" in rule:
                lo, hi = rule["rainfall_range"]
                if lo <= rainfall <= hi:
                    score += 0.10
                    reasons.append("Rainfall supports pest spread")

            # SEASON
            if "season" in rule and month_name in rule["season"]:
                score += 0.15
                reasons.append(f"Seasonal occurrence ({month_name})")

            # STAGE (do NOT penalize if unknown)
            if "stage" in rule:
                if not stage or stage in rule["stage"]:
                    score += 0.10
                    reasons.append("Crop stage susceptible")

            # SOIL
            if "soil" in rule:
                if not soilType or soilType in rule["soil"]:
                    score += 0.05

            # DISTRICT HISTORY (VERY IMPORTANT)
            if (
                district in self.pest_history and
                crop in self.pest_history[district] and
                pest_name in self.pest_history[district][crop]
            ):
                hist = self.pest_history[district][crop][pest_name]
                hist_score = self._history_score(hist.get("risk_level"))
                score += hist_score
                reasons.append(
                    f"Historical outbreaks in {district} ({hist.get('risk_level')})"
                )

            score = min(score, 1.0)

            alerts.append({
                "cropName": cropName,
                "pestName": pest_name,
                "riskLevel": self._risk_level(score),
                "score": round(score, 2),
                "reasons": reasons,
                "symptoms": rule.get("symptoms", ""),
                "preventive": rule.get("preventive", ""),
                "corrective": rule.get("corrective", "")
            })

        return alerts
