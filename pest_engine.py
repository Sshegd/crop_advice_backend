# pest_engine.py
from datetime import datetime

class PestEngine:

    def __init__(self, pest_db, district_history):
        self.pest_db = pest_db
        self.district_history = district_history

    def predict(self, crop_name, district):
        crop_key = crop_name.lower().strip()
        district_key = (district or "").lower().strip()

        alerts = []

        # 1️⃣ From PEST_DB
        crop_pests = self.pest_db.get(crop_key, {})
        for pest, rule in crop_pests.items():
            alerts.append({
                "pestName": pest,
                "riskLevel": "MEDIUM",
                "score": 0.6,
                "reasons": ["Weather & crop stage favourable"],
                "symptoms": rule.get("symptoms", ""),
                "preventive": rule.get("preventive", ""),
                "corrective": rule.get("corrective", "")
            })

        # 2️⃣ District history override
        district_data = self.district_history.get(district_key, {})
        hist = district_data.get(crop_key, {})
        for pest, info in hist.items():
            alerts.append({
                "pestName": pest,
                "riskLevel": info.get("risk_level", "HIGH"),
                "score": 0.85,
                "reasons": ["Reported outbreaks in your district"],
                "symptoms": crop_pests.get(pest, {}).get("symptoms", ""),
                "preventive": crop_pests.get(pest, {}).get("preventive", ""),
                "corrective": crop_pests.get(pest, {}).get("corrective", "")
            })

        return alerts
