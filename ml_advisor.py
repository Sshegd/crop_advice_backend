# ml_advisor.py
from typing import List, Dict, Any
import os
import numpy as np
import joblib
from ml_features import extract_features


# ----------------- Helper data for new crop advisory -----------------

# Approximate nutrient/pH/humidity profiles per soil type
SOIL_PROFILES = {
    "Red Soil":      {"N": 80, "P": 40, "K": 40, "ph": 6.5, "humidity": 70},
    "Black Soil":    {"N": 90, "P": 45, "K": 50, "ph": 7.2, "humidity": 65},
    "Laterite":      {"N": 75, "P": 35, "K": 40, "ph": 5.8, "humidity": 75},
    "Alluvial":      {"N": 85, "P": 42, "K": 45, "ph": 7.0, "humidity": 68},
    "Sandy":         {"N": 60, "P": 30, "K": 30, "ph": 6.2, "humidity": 60},
    "Loamy":         {"N": 88, "P": 44, "K": 46, "ph": 6.8, "humidity": 72},
}

DEFAULT_PROFILE = {"N": 85, "P": 40, "K": 40, "ph": 6.6, "humidity": 70}

# Advice templates per crop label (from Kaggle dataset labels)
CROP_TEMPLATES: Dict[str, Dict[str, str]] = {
    "rice": {
        "water": "Maintain standing water of 2–5 cm in early growth. Prefer puddled fields or controlled flooding.",
        "nutrient": "Apply 10–12 t/ha FYM before puddling. Use split N application (basal, tillering, panicle initiation) with balanced P & K.",
        "seed": "Use certified high-yielding varieties; ensure proper seed treatment and 2–3 cm sowing depth.",
        "other": "Keep fields weed-free in first 30–40 days; monitor for blast and BPH regularly.",
    },
    "wheat": {
        "water": "Give first irrigation at CRI stage (18–21 days) then at tillering, jointing, heading and milking depending on rainfall.",
        "nutrient": "Apply basal NPK at sowing; split remaining N in 2–3 doses. Avoid excess N to prevent lodging.",
        "seed": "Use bold, disease-free seeds of region-specific varieties; maintain recommended seed rate and spacing.",
        "other": "Timely sowing and weed management within 20–25 days are crucial for good yield.",
    },
    "maize": {
        "water": "Ensure adequate moisture at germination, tasseling and grain filling. Avoid waterlogging.",
        "nutrient": "Apply FYM + basal NPK and top-dress N in 2–3 splits. Zinc deficiency is common; apply ZnSO4 if needed.",
        "seed": "Select hybrid seed suitable for your season; maintain proper plant population.",
        "other": "Practice earthing-up and monitor for stem borer and foliar diseases.",
    },
    "chickpea": {
        "water": "Generally grown on conserved soil moisture; 1–2 life-saving irrigations at flowering/pod filling if needed.",
        "nutrient": "Apply basal P and moderate N; inoculate seed with Rhizobium culture for better nodulation.",
        "seed": "Use wilt-tolerant varieties; treat seed against seed-borne diseases.",
        "other": "Avoid waterlogging; practice wider spacing in heavy soils.",
    },
    "mango": {
        "water": "Irrigate young plants frequently; for bearing trees, irrigate at critical fruit development stages and avoid water stress.",
        "nutrient": "Apply FYM + NPK based on tree age, split between pre- and post-monsoon.",
        "seed": "Use grafted plants of recommended varieties; plant on raised pits with good drainage.",
        "other": "Regular pruning and pest/disease monitoring are essential for quality fruits.",
    },
    "banana": {
        "water": "Requires uniform moisture; adopt drip or basin irrigation. Avoid moisture stress especially during bunch initiation.",
        "nutrient": "High feeder crop – follow scheduled NPK fertigation plus FYM/compost mulching.",
        "seed": "Use tissue-cultured, disease-free planting material of high-yielding clones.",
        "other": "Provide propping, de-suckering and leaf sanitation to reduce disease pressure.",
    },
    # Add more crops as needed; others fall back to generic template
}

GENERIC_TEMPLATE = {
    "water": "Maintain adequate soil moisture without waterlogging; adjust based on rainfall and crop stage.",
    "nutrient": "Apply well-decomposed FYM before planting and follow a balanced NPK schedule with 2–3 split applications.",
    "seed": "Use certified, disease-free seeds or planting material of recommended high-yielding varieties.",
    "other": "Monitor pests and diseases regularly; keep field weed-free, especially in early growth stages.",
}


# ----------------- New crop advisor (ML-based) -----------------


class NewCropAdvisor:
    """
    ML-based crop recommendation using RandomForest model trained
    on Kaggle Crop Recommendation dataset (N, P, K, temperature, humidity, pH, rainfall).

    Model is saved as new_crop_model.pkl using train_new_crop_model.py
    and loaded here as a scikit-learn Pipeline.
    """

    def __init__(self, model_path: str = "new_crop_model.pkl"):
        self.model_path = model_path
        self.model_available = False
        self.model = None

        if os.path.exists(self.model_path):
            try:
                self.model = joblib.load(self.model_path)
                self.model_available = True
                print("Loaded new crop model from", self.model_path)
            except Exception as e:
                print("Failed to load model:", e)
        else:
            print("new_crop_model.pkl not found; using fallback recommendations.")

    def _build_features_from_payload(self, payload: Dict[str, Any]) -> np.ndarray:
        soil_type = (payload.get("soilType") or "").strip()
        profile = SOIL_PROFILES.get(soil_type, DEFAULT_PROFILE)

        N = float(profile["N"])
        P = float(profile["P"])
        K = float(profile["K"])
        ph = float(profile["ph"])
        humidity = float(profile["humidity"])

        temperature = float(payload.get("avgTemp", 26.0))
        rainfall = float(payload.get("avgRainfall", 2000.0))

        return np.array([[N, P, K, temperature, humidity, ph, rainfall]])

    def recommend(self, payload: Dict[str, Any], top_k: int = 3) -> List[Dict[str, Any]]:
        """
        payload: {
          "district": "...",
          "taluk": "...",
          "soilType": "Red Soil",
          "farmSizeAcre": 1.0,
          "avgRainfall": 2300,
          "avgTemp": 27
        }
        """
        if not self.model_available:
            # Fallback simple list if model is not present
            fallback = ["rice", "arecanut", "banana"]
            recommendations = []
            for name in fallback:
                tmpl = CROP_TEMPLATES.get(name, GENERIC_TEMPLATE)
                recommendations.append(
                    {
                        "cropName": name,
                        "score": 0.0,
                        "waterManagement": tmpl["water"],
                        "nutrientManagement": tmpl["nutrient"],
                        "seedSelection": tmpl["seed"],
                        "otherAdvice": tmpl["other"],
                    }
                )
            return recommendations

        X = self._build_features_from_payload(payload)
        proba = self.model.predict_proba(X)[0]
        classes = self.model.classes_

        # Top-k crops by probability
        idx_sorted = np.argsort(proba)[::-1][:top_k]

        recommendations: List[Dict[str, Any]] = []
        for idx in idx_sorted:
            crop_label = str(classes[idx])
            score = float(proba[idx])
            tmpl = CROP_TEMPLATES.get(crop_label, GENERIC_TEMPLATE)

            recommendations.append(
                {
                    "cropName": crop_label,
                    "score": score,
                    "waterManagement": tmpl["water"],
                    "nutrientManagement": tmpl["nutrient"],
                    "seedSelection": tmpl["seed"],
                    "otherAdvice": tmpl["other"],
                }
            )

        return recommendations


# ----------------- Existing crop advisor (Firebase logs) -----------------

class ExistingCropAdvisor:

    def __init__(self):
        self.model = None
        if os.path.exists("existing_crop_advice_model.pkl"):
            self.model = joblib.load("existing_crop_advice_model.pkl")

    def advise(self, logs, crop_name: str | None):

        crop = crop_name or "Unknown Crop"

        # -------- RULE FALLBACK (NO LOGS) --------
        if not logs:
            return {
                "cropName": crop,
                "cropManagement": ["Add farm activities to receive personalized advice."],
                "nutrientManagement": [],
                "waterManagement": [],
                "protectionManagement": [],
                "harvestMarketing": []
            }

        # -------- FEATURE EXTRACTION --------
        f = extract_features(logs, crop)

        X = [[
            f["soil_preparation"],
            f["sowing"],
            f["nutrient"],
            f["water"],
            f["protection"],
            f["harvest"]
        ]]

        # -------- ML PREDICTION --------
        if self.model:
            preds = self.model.predict(X)[0]
        else:
            preds = [1,1,1,1,1]   # safe fallback

        rec = {
            "cropManagement": [],
            "nutrientManagement": [],
            "waterManagement": [],
            "protectionManagement": [],
            "harvestMarketing": []
        }

        if preds[0]:
            rec["cropManagement"].append(
                f"Based on your field activities for {crop}, continue proper crop management practices."
            )
        if preds[1]:
            rec["nutrientManagement"].append(
                "Apply fertilizers in split doses according to crop stage and soil test."
            )
        if preds[2]:
            rec["waterManagement"].append(
                "Maintain optimum soil moisture; avoid water stress."
            )
        if preds[3]:
            rec["protectionManagement"].append(
                "Monitor pests and diseases regularly and apply control measures early."
            )
        if preds[4]:
            rec["harvestMarketing"].append(
                "Plan harvest at physiological maturity and monitor local market prices."
            )

        return {
            "cropName": crop,
            **rec
        }
