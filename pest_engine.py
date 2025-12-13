from datetime import datetime
from typing import Dict, Optional


class PestEngine:
    def __init__(self, pest_db: Dict, pest_history: Dict):
        self.pest_db = pest_db
        self.pest_history = pest_history

    def _month_name(self, month: Optional[int]):
        if not month:
            month = datetime.utcnow().month
        return datetime(2000, month, 1).strftime("%B")

    def predict(
        self,
        cropName: str,
        district: str = None,
        soilType: str = None,
        stage: str = None,
        temp: float = None,
        humidity: float = None,
        month_int: int = None,
    ):
        crop = cropName.lower().strip()
        district = district.lower().strip() if district else None
        soilType = soilType.lower().strip() if soilType else None
        stage = stage.lower().strip() if stage else None

        if crop not in self.pest_db:
            return []

        month_name = self._month_name(month_int)
        alerts = []

        for pest, rule in self.pest_db[crop].items():
            score = 0
            reasons = []

            if temp and "temp_range" in rule:
                lo, hi = rule["temp_range"]
                if lo <= temp <= hi:
                    score += 1
                    reasons.append("Temperature favorable")

            if humidity and "humidity_gt" in rule:
                if humidity > rule["humidity_gt"]:
                    score += 1
                    reasons.append("Humidity favorable")

            if month_name in rule.get("season", []):
                score += 1
                reasons.append("Season favorable")

            if stage and stage in rule.get("stage", []):
                score += 1
                reasons.append("Crop stage favorable")

            if soilType and soilType in rule.get("soil", []):
                score += 1
                reasons.append("Soil suitable")

            if (
                district
                and district in self.pest_history
                and crop in self.pest_history[district]
                and pest in self.pest_history[district][crop]
            ):
                score += 1
                reasons.append("Historical risk in district")

            if score >= 2:
                alerts.append({
                    "cropName": cropName,
                    "pestName": pest,
                    "riskLevel": "HIGH" if score >= 4 else "MEDIUM",
                    "score": score,
                    "reasons": reasons,
                    "symptoms": rule["symptoms"],
                    "preventive": rule["preventive"],
                    "corrective": rule["corrective"],
                })

        if not alerts:
            alerts.append({
                "cropName": cropName,
                "pestName": "General Pest Advisory",
                "riskLevel": "LOW",
                "score": 1,
                "reasons": ["Conditions not severe for major pests"],
                "symptoms": "",
                "preventive": "Continue monitoring",
                "corrective": ""
            })

        return alerts
