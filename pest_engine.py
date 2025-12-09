# pest_engine.py
# ==========================================================
# FULL Pest Detection Engine
# Uses:
#   - pest_db.py (20-crop ICAR pest dataset)
#   - district_pest_history.py (31 district patterns)
#   - google_translate.py
# ==========================================================

from datetime import datetime
from typing import Dict, Optional, List
from pest_db import PEST_DB
from district_pest_history import PEST_HISTORY
from google_translate import translate_text


class PestEngine:

    # -------------------------------
    # Convert int month → Month name
    # -------------------------------
    def get_month_name(self, month_int: Optional[int]):
        if month_int is None:
            month_int = datetime.utcnow().month
        return datetime(2000, month_int, 1).strftime("%B")

    # -------------------------------
    # Evaluate a single pest rule set
    # -------------------------------
    def evaluate_rule(self,
                      rule: Dict,
                      crop_stage: Optional[str],
                      temp: Optional[float],
                      hum: Optional[float],
                      rain: Optional[float],
                      month_name: str,
                      symptoms_text: Optional[str]):

        reasons = []
        total_cond = 0
        matched = 0

        # temp > X
        if "temp_gt" in rule and temp is not None:
            total_cond += 1
            if temp > rule["temp_gt"]:
                matched += 1
                reasons.append(f"Temperature {temp}°C > {rule['temp_gt']}°C")

        # temp range
        if "temp_range" in rule and temp is not None:
            total_cond += 1
            lo, hi = rule["temp_range"]
            if lo <= temp <= hi:
                matched += 1
                reasons.append(f"Temp {temp}°C within {lo}-{hi}°C")

        # humidity >
        if "humidity_gt" in rule and hum is not None:
            total_cond += 1
            if hum > rule["humidity_gt"]:
                matched += 1
                reasons.append(f"Humidity {hum}% > {rule['humidity_gt']}%")

        # humidity <
        if "humidity_lt" in rule and hum is not None:
            total_cond += 1
            if hum < rule["humidity_lt"]:
                matched += 1
                reasons.append(f"Humidity {hum}% < {rule['humidity_lt']}%")

        # rainfall >
        if "rainfall_gt" in rule and rain is not None:
            total_cond += 1
            if rain > rule["rainfall_gt"]:
                matched += 1
                reasons.append(f"Rainfall {rain}mm > {rule['rainfall_gt']}mm")

        # rainfall <
        if "rainfall_lt" in rule and rain is not None:
            total_cond += 1
            if rain < rule["rainfall_lt"]:
                matched += 1
                reasons.append(f"Rainfall {rain}mm < {rule['rainfall_lt']}mm")

        # crop stage
        if "stage" in rule and crop_stage:
            total_cond += 1
            if crop_stage in rule["stage"]:
                matched += 1
                reasons.append(f"Crop stage risk: {crop_stage}")

        # season match
        if "season" in rule:
            total_cond += 1
            if month_name in rule["season"]:
                matched += 1
                reasons.append(f"Season risk in {month_name}")

        # core rule score
        score = (matched / total_cond) if total_cond > 0 else 0

        # textual symptom clue (+15%)
        if symptoms_text:
            possible_words = rule.get("symptoms", "").lower().split()
            text = symptoms_text.lower()
            if any(w in text for w in possible_words):
                score = min(1.0, score + 0.15)
                reasons.append("Farmer symptom text matches pest profile")

        return score, reasons

    # -------------------------------
    # Apply District History Boost
    # -------------------------------
    def apply_district_history(self, district: str,
                               crop: str,
                               pest_name: str,
                               month_name: str,
                               score: float,
                               reasons: List[str]):

        d = district.lower()
        crop = crop.lower()

        hist = PEST_HISTORY.get(d, {}).get(crop, {}).get(pest_name)
        if not hist:
            return score, reasons

        # Season boost
        if month_name in hist.get("season", []):
            score += 0.20
            reasons.append(f"Historically occurs in {d.title()} during {month_name}")

        # Peak month boost
        if month_name in hist.get("peak_months", []):
            score += 0.35
            reasons.append(f"Peak outbreak month in {d.title()}")

        # Base district risk
        rl = hist.get("risk_level")
        if rl == "HIGH":
            score += 0.20
        elif rl == "MEDIUM":
            score += 0.10

        return min(1.0, score), reasons

    # -------------------------------
    # Convert numeric score → Risk
    # -------------------------------
    def risk_tag(self, score: float):
        if score >= 0.75: return "HIGH"
        if score >= 0.45: return "MEDIUM"
        return "LOW"

    # ==========================================================
    # Main Pest Detection Function
    # ==========================================================
    def detect(self,
               crop: str,
               district: Optional[str],
               taluk: Optional[str],
               crop_stage: Optional[str],
               temp: Optional[float],
               humidity: Optional[float],
               rainfall: Optional[float],
               month: Optional[int],
               symptoms_text: Optional[str],
               lang: str):

        crop = crop.lower().strip()
        month_name = self.get_month_name(month)

        if crop not in PEST_DB:
            return []

        results = []

        for pest_name, rule in PEST_DB[crop].items():

            # 1) rule-based evaluation
            score, reasons = self.evaluate_rule(rule,
                                                crop_stage,
                                                temp,
                                                humidity,
                                                rainfall,
                                                month_name,
                                                symptoms_text)

            # 2) add district-history boost
            if district:
                score, reasons = self.apply_district_history(district,
                                                             crop,
                                                             pest_name,
                                                             month_name,
                                                             score,
                                                             reasons)

            if score < 0.40:
                continue  # ignore weak matches

            risk = self.risk_tag(score)

            # translation
            symptoms = rule.get("symptoms", "")
            preventive = rule.get("preventive", "")
            corrective = rule.get("corrective", "")

            if lang != "en":
                try:
                    pest_name = translate_text(pest_name, lang)
                    symptoms = translate_text(symptoms, lang)
                    preventive = translate_text(preventive, lang)
                    corrective = translate_text(corrective, lang)
                except:
                    pass

            results.append({
                "pestName": pest_name,
                "riskLevel": risk,
                "score": round(score, 2),
                "reasons": reasons,
                "symptoms": symptoms,
                "preventive": preventive,
                "corrective": corrective
            })

        return results
