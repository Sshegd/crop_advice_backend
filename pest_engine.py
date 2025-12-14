# pest_engine.py
from typing import Dict, List, Optional
from datetime import datetime
from firebase_admin import db


class PestEngine:
    def __init__(self, pest_db: Dict, pest_history: Dict, firebase_db):
        """
        pest_db       → Rule-based pest knowledge
        pest_history  → District-wise historical risk
        firebase_db   → firebase_admin.db
        """
        self.pest_db = pest_db
        self.pest_history = pest_history
        self.firebase_db = firebase_db

    # --------------------------------------------------
    # FIREBASE DATA FETCH
    # --------------------------------------------------

    def _get_user_farm_data(self, user_id: str):
        ref = self.firebase_db.reference(f"Users/{user_id}")
        user = ref.get()

        if not user:
            return None

        farm = user.get("farmDetails", {})
        primary_logs = user.get("farmActivityLogs", {})
        secondary = user.get("secondaryCrops", {})

        crops = []

        # PRIMARY CROP
        if farm.get("cropName"):
            crops.append({
                "cropName": farm.get("cropName"),
                "activityLogs": list(primary_logs.values())
            })

        # SECONDARY CROPS
        for crop_name, data in secondary.items():
            crops.append({
                "cropName": crop_name,
                "activityLogs": list(data.get("activityLogs", {}).values())
            })

        return {
            "district": farm.get("district"),
            "soilType": farm.get("soilType"),
            "crops": crops
        }

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------

    def _extract_latest_stage(self, logs: List[dict]) -> Optional[str]:
        if not logs:
            return None

        latest = sorted(
            logs,
            key=lambda x: x.get("timestamp", 0),
            reverse=True
        )[0]

        return latest.get("stage")

    def _month_name(self, month_int: Optional[int]) -> str:
        if not month_int:
            month_int = datetime.now().month
        return datetime(2000, month_int, 1).strftime("%B")

    def _risk_level(self, score: float) -> str:
        if score >= 0.75:
            return "HIGH"
        if score >= 0.45:
            return "MEDIUM"
        return "LOW"

    # --------------------------------------------------
    # RULE EVALUATION
    # --------------------------------------------------

    def _evaluate_rule(
        self,
        rule: Dict,
        stage: Optional[str],
        temp: Optional[float],
        humidity: Optional[float],
        rainfall: Optional[float],
        month_name: str
    ):
        matched = 0
        total = 0
        reasons = []

        if "temp_range" in rule and temp is not None:
            total += 1
            lo, hi = rule["temp_range"]
            if lo <= temp <= hi:
                matched += 1
                reasons.append(f"Temperature {temp}°C suitable")

        if "humidity_gt" in rule and humidity is not None:
            total += 1
            if humidity > rule["humidity_gt"]:
                matched += 1
                reasons.append(f"High humidity {humidity}%")

        if "rainfall_gt" in rule and rainfall is not None:
            total += 1
            if rainfall > rule["rainfall_gt"]:
                matched += 1
                reasons.append("Heavy rainfall conditions")

        if "season" in rule:
            total += 1
            if month_name in rule["season"]:
                matched += 1
                reasons.append(f"Season: {month_name}")

        if "stage" in rule and stage:
            total += 1
            if stage in rule["stage"]:
                matched += 1
                reasons.append(f"Crop stage: {stage}")

        score = matched / total if total else 0
        return score, reasons

    # --------------------------------------------------
    # MAIN PEST PREDICTION (FULL AUTO)
    # --------------------------------------------------

    def predict_for_user(
        self,
        user_id: str,
        temp: Optional[float] = None,
        humidity: Optional[float] = None,
        rainfall: Optional[float] = None,
        month_int: Optional[int] = None,
        lang: str = "en"
    ) -> List[dict]:

        data = self._get_user_farm_data(user_id)
        if not data:
            return []

        district = (data["district"] or "").lower()
        soil = (data["soilType"] or "").lower()
        month_name = self._month_name(month_int)

        alerts = []

        for crop in data["crops"]:
            crop_name = crop["cropName"]
            crop_key = crop_name.lower().strip()
            stage = self._extract_latest_stage(crop["activityLogs"])

            if crop_key not in self.pest_db:
                continue

            for pest_name, rule in self.pest_db[crop_key].items():
                score, reasons = self._evaluate_rule(
                    rule, stage, temp, humidity, rainfall, month_name
                )

                # DISTRICT HISTORY BOOST
                if (
                    district in self.pest_history and
                    crop_key in self.pest_history[district] and
                    pest_name in self.pest_history[district][crop_key]
                ):
                    hist = self.pest_history[district][crop_key][pest_name]
                    score = min(1.0, score + hist * 0.25)
                    reasons.append("Historical outbreak in district")

                if score < 0.45:
                    continue

                alerts.append({
                    "cropName": crop_name,
                    "pestName": pest_name,
                    "riskLevel": self._risk_level(score),
                    "score": round(score, 2),
                    "reasons": reasons,
                    "symptoms": rule.get("symptoms", ""),
                    "preventive": rule.get("preventive", ""),
                    "corrective": rule.get("corrective", "")
                })

        return alerts
