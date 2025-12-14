# pest_engine.py
from datetime import datetime
from typing import Dict, List


class PestEngine:
    def __init__(self, pest_db: Dict, district_history: Dict):
        self.pest_db = pest_db
        self.district_history = district_history

    def _risk_level(self, score: float) -> str:
        if score >= 0.7:
            return "HIGH"
        if score >= 0.4:
            return "MEDIUM"
        return "LOW"

    def predict(
        self,
        cropName: str,
        district: str = None,
        soilType: str = None,
        month: int = None
    ) -> List[Dict]:

        crop_key = cropName.lower().strip()
        if crop_key not in self.pest_db:
            return []

        month_name = datetime(2000, month or datetime.now().month, 1).strftime("%B")
        alerts = []

        for pest_name, rule in self.pest_db[crop_key].items():
            score = 0.0
            reasons = []

            # 1️⃣ District history (STRONG SIGNAL)
            if district:
                d = district.lower()
                if d in self.district_history:
                    if crop_key in self.district_history[d]:
                        if pest_name in self.district_history[d][crop_key]:
                            score += 0.5
                            reasons.append("Frequently reported in your district")

            # 2️⃣ Seasonal relevance
            if "season" in rule and month_name in rule["season"]:
                score += 0.3
                reasons.append(f"Common during {month_name}")

            # 3️⃣ Soil suitability
            if soilType and "soil" in rule:
                if soilType.lower() in [s.lower() for s in rule["soil"]]:
                    score += 0.2
                    reasons.append("Soil conditions favor this pest")

            # 🚨 MINIMUM ADVISORY THRESHOLD
            if score < 0.4:
                continue

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
