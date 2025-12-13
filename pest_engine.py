# pest_engine.py
from typing import Dict, Optional
from datetime import datetime


class PestEngine:
    def __init__(self, pest_db: Dict, pest_history: Dict):
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

    # -----------------------------
    # RULE EVALUATION
    # -----------------------------
    def _evaluate_rule(
        self,
        rule: Dict,
        stage: Optional[str],
        temp: Optional[float],
        hum: Optional[float],
        rain: Optional[float],
        month_name: str,
        soilType: Optional[str],
        symptoms_text: Optional[str],
    ):
        reasons = []
        matched = 0
        total = 0

        # 🌡 Temperature
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
                reasons.append(f"Temperature {temp} in range {lo}-{hi}")

        # 💧 Humidity
        if "humidity_gt" in rule and hum is not None:
            total += 1
            if hum > rule["humidity_gt"]:
                matched += 1
                reasons.append(f"Humidity {hum}% > {rule['humidity_gt']}%")

        if "humidity_lt" in rule and hum is not None:
            total += 1
            if hum < rule["humidity_lt"]:
                matched += 1
                reasons.append(f"Humidity {hum}% < {rule['humidity_lt']}%")

        # 🌧 Rainfall
        if "rainfall_range" in rule and rain is not None:
            total += 1
             lo, hi = rule["rainfall_range"]
            if rain <= rain<=hi:
                matched += 1
                reasons.append(f"Rainfall {rain}mm > in {lo}-{hi}mm")

        if "rainfall_gt" in rule and rain is not None:
            total += 1
            if rain > rule["rainfall_gt"]:
                matched += 1
                reasons.append(f"Rainfall {rain}mm > {rule['rainfall_gt']}mm")
                
        if "rainfall_lt" in rule and rain is not None:
            total += 1
            if rain < rule["rainfall_lt"]:
                matched += 1
                reasons.append(f"Rainfall {rain}mm < {rule['rainfall_lt']}mm")

        # 🗓 Season
        if "season" in rule:
            total += 1
            if month_name in rule["season"]:
                matched += 1
                reasons.append(f"Season: {month_name}")

        # 🌱 Crop stage
        if "stage" in rule and stage:
            total += 1
            if stage in rule["stage"]:
                matched += 1
                reasons.append(f"Crop stage: {stage}")

        # 🌍 Soil type (IMPORTANT FIX)
        if "soil" in rule and soilType:
            total += 1
            if soilType in rule["soil"]:
                matched += 1
                reasons.append(f"Soil matched: {soilType}")
        

        # 📊 Base score
        score = matched / total if total > 0 else 0.0

        # 📝 Symptom text boost (optional)
        if symptoms_text:
            symptom_words = rule.get("symptoms", "").lower().split()
            text = symptoms_text.lower()
            if any(word in text for word in symptom_words):
                score = min(1.0, score + 0.20)
                reasons.append("Farmer-reported symptoms match")

        return score, reasons

    # -----------------------------
    # MAIN PREDICTION ENGINE
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
        district = district.lower().strip() if district else None
        soilType = soilType.lower().strip() if soilType else None
        stage = stage.lower().strip() if stage else None

        if crop not in self.pest_db:
            return []

        month_name = self._month_name(month_int)
        alerts = []

        for pest_name, rule in self.pest_db[crop].items():
            score, reasons = self._evaluate_rule(
                rule,
                stage,
                temp,
                humidity,
                rainfall,
                month_name,
                soilType,
                None,
            )

            # 📍 District history boost
            if (
                district
                and district in self.pest_history
                and crop in self.pest_history[district]
                and pest_name in self.pest_history[district][crop]
            ):
                risk = self.pest_history[district][crop][pest_name]["risk_level"]
                boost_map = {"LOW": 0.10, "MEDIUM": 0.20, "HIGH": 0.30}
                boost = boost_map.get(risk, 0)
                score = min(1.0, score + boost)
                reasons.append(f"Historical risk in {district}: {risk}")

            # ⚠ Lower threshold for early warning
            if score < 0.30:
                continue

            alerts.append({
                "cropName": cropName,
                "pestName": pest_name,
                "riskLevel": self._risk_level(score),
                "score": round(score, 2),
                "reasons": reasons,
                "symptoms": rule.get("symptoms", ""),
                "preventive": rule.get("preventive", ""),
                "corrective": rule.get("corrective", ""),
            })

        # 🟢 Fallback (important UX)
        if not alerts:
            return [{
                "cropName": cropName,
                "pestName": "No major pest outbreak detected",
                "riskLevel": "LOW",
                "score": 0.2,
                "reasons": ["Current conditions are not favorable for major pests"],
                "symptoms": "",
                "preventive": "Continue regular field monitoring and sanitation.",
                "corrective": ""
            }]

        return alerts

