# pest_engine.py
from typing import List, Dict, Optional
from datetime import datetime


class PestEngine:
    def __init__(self, pest_db: Dict, pest_history: Dict):
        """
        Accepts:
            pest_db      - Full ICAR Karnataka pest knowledge base
            pest_history - 20-year district outbreak probabilities
        """
        self.pest_db = pest_db
        self.pest_history = pest_history


    # -----------------------------
    # INTERNAL HELPERS
    # -----------------------------
    def _month_name(self, month_int: Optional[int]) -> str:
        if month_int is None:
            month_int = datetime.utcnow().month
        return datetime(2000, month_int, 1).strftime("%B")


    def _risk_level(self, score: float) -> str:
        if score >= 0.75:
            return "HIGH"
        if score >= 0.45:
            return "MEDIUM"
        return "LOW"


    def _evaluate_rule(self, rule: Dict, stage, temp, hum, rain, month_name, symptoms_text):
        """Returns: (score: float, reasons: list[str])"""
        reasons = []
        matched = 0
        total = 0

        # temperature
        if "temp_gt" in rule and temp is not None:
            total += 1
            if temp > rule["temp_gt"]:
                matched += 1
                reasons.append(f"Temperature {temp} > {rule['temp_gt']}")

        if "temp_range" in rule and temp is not None:
            total += 1
            lo, hi = rule["temp_range"]
            if lo <= temp <= hi:
                matched += 1
                reasons.append(f"Temperature {temp} in {lo}-{hi}")

        # humidity
        if "humidity_gt" in rule and hum is not None:
            total += 1
            if hum > rule["humidity_gt"]:
                matched += 1
                reasons.append(f"Humidity {hum} > {rule['humidity_gt']}")

        if "humidity_lt" in rule and hum is not None:
            total += 1
            if hum < rule["humidity_lt"]:
                matched += 1
                reasons.append(f"Humidity {hum} < {rule['humidity_lt']}")

        # rainfall
        if "rainfall_gt" in rule and rain is not None:
            total += 1
            if rain > rule["rainfall_gt"]:
                matched += 1
                reasons.append(f"Rainfall {rain} > {rule['rainfall_gt']}")

        if "rainfall_lt" in rule and rain is not None:
            total += 1
            if rain < rule["rainfall_lt"]:
                matched += 1
                reasons.append(f"Rainfall {rain} < {rule['rainfall_lt']}")

        # season
        if "season" in rule:
            total += 1
            if month_name in rule["season"]:
                matched += 1
                reasons.append(f"Season: {month_name}")

        # stage of crop
        if "stage" in rule and stage:
            total += 1
            if stage in rule["stage"]:
                matched += 1
                reasons.append(f"Crop stage: {stage}")

        # symptoms boost
        score = matched / total if total > 0 else 0

        if symptoms_text:
            symptom_words = rule.get("symptoms", "").lower().split()
            text = symptoms_text.lower()

            if any(word in text for word in symptom_words):
                score = min(1.0, score + 0.20)  # 20% confidence boost
                reasons.append("Farmer symptom text suggests relevance")

        return score, reasons


    # -----------------------------
    # MAIN API ENGINE
    # -----------------------------
    def predict(
        self,
        cropName: str,
        district: str = None,
        taluk: str = None,
        soilType: str = None,
        stage: str = None,
        temp: float = None,
        humidity: float = None,
        rainfall: float = None,
        month_int: int = None,
        lang: str = "en",
    ):
        crop = cropName.lower().strip()
        month_name = self._month_name(month_int)

        if crop not in self.pest_db:
            return []

        alerts = []

        # 1. Loop pests for this crop
        for pest_name, rule in self.pest_db[crop].items():
            score, reasons = self._evaluate_rule(
                rule,
                stage,
                temp,
                humidity,
                rainfall,
                month_name,
                None   # symptoms text not needed here
            )

            # 2. Add district outbreak history boost
            if district in self.pest_history and crop in self.pest_history[district]:
                if pest_name in self.pest_history[district][crop]:
                    historical_risk = self.pest_history[district][crop][pest_name]
                    score = min(1.0, score + historical_risk * 0.25)
                    reasons.append(f"Historical outbreak risk: {historical_risk}")

            if score < 0.45:  
                continue

            # 3. Prepare alert
            risk_level = self._risk_level(score)

            symptoms = rule.get("symptoms", "")
            preventive = rule.get("preventive", "")
            corrective = rule.get("corrective", "")

        

            alerts.append({
                "cropName": cropName,
                "pestName": pest_name,
                "riskLevel": self._risk_level(score),
                "score": round(score, 2),
                "reasons": reasons,
                "symptoms": rule.get("symptoms", []),
                "preventive": rule.get("preventive", []),
                "corrective": rule.get("corrective", [])
            })


        return alerts

