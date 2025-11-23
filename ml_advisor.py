# ml_advisor.py
from typing import List, Dict, Any
import os
import numpy as np
import joblib


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
    """
    Advisory using Firebase activity logs for the existing crop.

    Input: list of log dicts (flattened from Users/{uid}/farmActivityLogs/primary_crop)
    and farm_details dict from Users/{uid}/farmDetails.

    Output: structured advice grouped by management area.
    """

    def __init__(self):
        pass  # placeholder if you later load an ML model

    def advise(
        self, farm_logs: List[Dict[str, Any]], farm_details: Dict[str, Any]
    ) -> Dict[str, Any]:
        crop_name = farm_details.get("cropName", "crop")

        # Extract important log entries by subActivity
        soil_prep_log = next(
            (log for log in farm_logs if log.get("subActivity") == "soil_preparation"),
            None,
        )
        water_log = next(
            (log for log in farm_logs if log.get("subActivity") == "water_management"),
            None,
        )
        nutrient_log = next(
            (
                log
                for log in farm_logs
                if log.get("subActivity") == "nutrient_management"
            ),
            None,
        )
        protection_log = next(
            (
                log
                for log in farm_logs
                if log.get("subActivity") == "crop_protection_maintenance"
            ),
            None,
        )
        harvest_log = next(
            (
                log
                for log in farm_logs
                if log.get("subActivity") == "harvesting_cut_gather"
            ),
            None,
        )
        marketing_log = next(
            (
                log
                for log in farm_logs
                if log.get("subActivity") == "marketing_distribution"
            ),
            None,
        )

        crop_management_tips: List[str] = []
        nutrient_tips: List[str] = []
        water_tips: List[str] = []
        protection_tips: List[str] = []
        marketing_tips: List[str] = []

        # -------- Soil & crop management --------
        if soil_prep_log:
            soil_test_done = soil_prep_log.get("soilTestDone", False)
            base_fert = soil_prep_log.get("baseFertilizer")
            if soil_test_done:
                soil = soil_prep_log.get("soilTest", {})
                pH = soil.get("pH")
                if pH is not None and (pH < 5.5 or pH > 7.5):
                    crop_management_tips.append(
                        f"Recorded soil pH is {pH}. Move it towards neutral using lime (for low pH) "
                        "or organic matter/gypsum (for high pH) as per local recommendation."
                    )
                else:
                    crop_management_tips.append(
                        "Soil testing is recorded. Continue testing every 2–3 years to refine fertilizer doses."
                    )
            else:
                crop_management_tips.append(
                    "No soil testing found in your logs. Consider doing a soil test before next season to "
                    "optimize fertilizer use and improve yield."
                )

            if base_fert:
                crop_management_tips.append(
                    f"Base FYM application of {base_fert.get('quantity','recommended dose')} on "
                    f"{base_fert.get('date','recorded date')} is good. Ensure thorough mixing into the soil."
                )
        else:
            crop_management_tips.append(
                "No soil preparation activity found. Ensure proper ploughing, levelling and FYM application "
                "before planting for better root growth."
            )

        # -------- Water management --------
        if water_log:
            freq = water_log.get("frequencyDays")
            methods = ", ".join(water_log.get("methods", []))
            water_tips.append(
                f"Irrigation every {freq} days using {methods} is recorded. "
                "Adjust frequency based on rainfall and soil moisture; avoid both drought and waterlogging."
            )
            if freq and freq > 10:
                water_tips.append(
                    "For young plants, long irrigation gaps (>10 days) may stress the crop. "
                    "Consider slightly shorter intervals during dry periods."
                )
        else:
            water_tips.append(
                "No water management logs found. Record irrigation schedule and ensure the crop "
                "does not face moisture stress during critical stages."
            )

        # -------- Nutrient management --------
        if nutrient_log and nutrient_log.get("applications"):
            apps = nutrient_log["applications"]
            names = [a.get("fertilizerName", "").lower() for a in apps]

            if any("urea" in n for n in names):
                nutrient_tips.append(
                    "Urea application is planned. Apply in split doses and incorporate into soil or irrigate immediately "
                    "to reduce nitrogen loss."
                )
            if any("dap" in n for n in names):
                nutrient_tips.append(
                    "DAP is planned. Avoid excessive DAP; balance with potash and organic manures to prevent nutrient imbalance."
                )

            nutrient_tips.append(
                "Keep a yearly nutrient plan with 2–3 split applications of N and K plus basal P and FYM. "
                "Use soil/leaf test reports to fine-tune doses."
            )
        else:
            nutrient_tips.append(
                "No fertilizer application found in logs. Prepare a crop-wise fertilizer schedule and record each application."
            )

        # -------- Crop protection --------
        if protection_log and protection_log.get("controlTaken"):
            prod = protection_log.get("controlDetails", {}).get("productName", "")
            pest = protection_log.get("pestDiseaseName", "")
            protection_tips.append(
                f"Pest/disease '{pest}' recorded and control with '{prod}' is noted. "
                "Continue regular field scouting and follow integrated pest management (IPM) practices."
            )
        else:
            protection_tips.append(
                "No crop protection records. Inspect the crop weekly for pests and diseases and record any sprays taken."
            )

        # -------- Harvest & marketing --------
        if harvest_log:
            qty = harvest_log.get("yieldQuantity")
            unit = harvest_log.get("yieldUnit", "")
            grade = harvest_log.get("grade", "")
            marketing_tips.append(
                f"Harvest of about {qty} {unit} (grade {grade}) is recorded. "
                "Compare this with local average yields to identify improvement scope."
            )
        if marketing_log:
            buyer = marketing_log.get("buyer", "")
            price = marketing_log.get("pricePerUnit")
            unit = marketing_log.get("quantityUnit", "")
            marketing_tips.append(
                f"Sale to {buyer} at ₹{price} per {unit} is recorded. "
                "Compare prices from different buyers/FPOs and explore storage or staggered sales to improve returns."
            )
        if not marketing_log and not harvest_log:
            marketing_tips.append(
                "No harvest/marketing data in logs. Record yield and sale details to analyse profitability in future seasons."
            )

        return {
            "cropName": crop_name,
            "cropManagement": crop_management_tips,
            "nutrientManagement": nutrient_tips,
            "waterManagement": water_tips,
            "protectionManagement": protection_tips,
            "harvestMarketing": marketing_tips,
        }
