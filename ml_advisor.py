# ml_advisor.py
from typing import List, Dict, Any
import numpy as np
import joblib

class NewCropAdvisor:
    """
    ML-based crop recommendation.
    Assumes `new_crop_model.pkl` is a scikit-learn classifier that predicts crop_name
    and has predict_proba for probabilities.
    Encoders.pkl should contain LabelEncoders / OneHotEncoders, etc.
    """
    def __init__(self, model_path: str = "new_crop_model.pkl", encoders_path: str = "encoders.pkl"):
        self.model = joblib.load(model_path)
        self.encoders = joblib.load(encoders_path)

    def _encode_features(self, payload: Dict[str, Any]) -> np.ndarray:
        """
        Turn incoming JSON into the feature vector for the ML model.
        You must match this with how you trained your model.
        Example features: district, taluk, soilType, farmSizeAcre, avgRainfall, avgTemp, etc.
        """
        # Example – adapt to your training pipeline
        district = payload.get("district", "")
        taluk = payload.get("taluk", "")
        soil_type = payload.get("soilType", "")
        farm_size = float(payload.get("farmSizeAcre", 1.0))
        avg_rainfall = float(payload.get("avgRainfall", 2000))
        avg_temp = float(payload.get("avgTemp", 26))

        # categorical encoders from encoders.pkl (LabelEncoder, OneHotEncoder, etc.)
        dist_idx = self.encoders["district"].transform([district])[0]
        taluk_idx = self.encoders["taluk"].transform([taluk])[0]
        soil_idx = self.encoders["soilType"].transform([soil_type])[0]

        X = np.array([[dist_idx, taluk_idx, soil_idx, farm_size, avg_rainfall, avg_temp]])
        return X

    def recommend(self, payload: Dict[str, Any], top_k: int = 3) -> List[Dict[str, Any]]:
        X = self._encode_features(payload)

        # predicted crop probabilities
        proba = self.model.predict_proba(X)[0]
        classes = self.model.classes_

        # sort by probability
        idx_sorted = np.argsort(proba)[::-1][:top_k]

        recommendations = []
        for idx in idx_sorted:
            crop_name = classes[idx]
            score = float(proba[idx])

            # These parts are *templated text* based on the selected crop.
            # The selection itself (crop_name + score) is ML-based.
            water_advice = (
                f"For {crop_name}, maintain soil moisture without waterlogging. "
                f"Use drip or basin irrigation suited to {payload.get('soilType', 'your soil')}."
            )
            nutrient_advice = (
                f"Follow a balanced NPK schedule for {crop_name}. Apply well-decomposed FYM "
                f"before planting and split application of N and K during growth."
            )
            seed_advice = (
                f"Choose high-yielding, disease-tolerant varieties of {crop_name} from certified nurseries/seed dealers. "
                f"Use healthy seed/seedlings only."
            )
            other_advice = (
                f"Plan timely weed management and pest-disease monitoring for {crop_name}. "
                f"Use mulching and organic matter to improve soil structure."
            )

            recommendations.append({
                "cropName": crop_name,
                "score": score,
                "waterManagement": water_advice,
                "nutrientManagement": nutrient_advice,
                "seedSelection": seed_advice,
                "otherAdvice": other_advice,
            })

        return recommendations


class ExistingCropAdvisor:
    """
    Advisory using Firebase activity logs.
    Here we don’t force ML; you can later plug in a trained model.
    For now we *summarise* management gaps using heuristics on logs.
    """
    def __init__(self):
        # If you train an ML model for existing crop management,
        # load it here, e.g. self.model = joblib.load("existing_crop_model.pkl")
        pass

    def advise(self, farm_logs: List[Dict[str, Any]], farm_details: Dict[str, Any]) -> Dict[str, Any]:
        crop_name = farm_details.get("cropName", "crop")

        # Pre-planting checks
        soil_test_done = any(
            log.get("subActivity") == "soil_preparation" and log.get("soilTestDone")
            for log in farm_logs
        )

        base_fertilizer = None
        for log in farm_logs:
            if log.get("subActivity") == "soil_preparation":
                base_fertilizer = log.get("baseFertilizer")
                break

        # Water management logs
        irrigation_log = next(
            (log for log in farm_logs if log.get("subActivity") == "water_management"),
            None
        )

        # Nutrient management logs
        nutrient_logs = next(
            (log for log in farm_logs if log.get("subActivity") == "nutrient_management"),
            None
        )

        # Pest / disease logs
        protection_log = next(
            (log for log in farm_logs if log.get("subActivity") == "crop_protection_maintenance"),
            None
        )

        # Harvest & marketing logs
        harvest_log = next(
            (log for log in farm_logs if log.get("subActivity") == "harvesting_cut_gather"),
            None
        )
        marketing_log = next(
            (log for log in farm_logs if log.get("subActivity") == "marketing_distribution"),
            None
        )

        crop_management_tips = []
        nutrient_tips = []
        water_tips = []
        protection_tips = []
        marketing_tips = []

        # ---------- CROP / SOIL MANAGEMENT ----------
        if not soil_test_done:
            crop_management_tips.append(
                "Soil testing not found in your logs. Conduct a soil test to fine-tune fertilizer doses."
            )
        else:
            st = next(log for log in farm_logs if log.get("subActivity") == "soil_preparation")
            soil = st.get("soilTest", {})
            pH = soil.get("pH")
            if pH and (pH < 5.5 or pH > 7.5):
                crop_management_tips.append(
                    f"Your recorded soil pH is {pH}. Consider liming (for low pH) or organic matter addition (for high pH) to bring it near neutral."
                )

        if base_fertilizer:
            crop_management_tips.append(
                f"Base fertilizer FYM of {base_fertilizer.get('quantity', 'recommended dose')} on {base_fertilizer.get('date', '')} is good. "
                "Ensure it is well decomposed and uniformly applied."
            )

        # ---------- WATER MANAGEMENT ----------
        if irrigation_log:
            freq = irrigation_log.get("frequencyDays")
            methods = ", ".join(irrigation_log.get("methods", []))
            water_tips.append(
                f"Irrigation is recorded every {freq} days using {methods}. "
                "Adjust frequency based on rainfall and soil moisture; reduce during heavy rains and increase during dry spells."
            )
        else:
            water_tips.append(
                "No water management logs found. Record irrigation schedule and ensure young plants never face moisture stress."
            )

        # ---------- NUTRIENT MANAGEMENT ----------
        if nutrient_logs and nutrient_logs.get("applications"):
            apps = nutrient_logs["applications"]
            urea_apps = [a for a in apps if "urea" in a.get("fertilizerName", "").lower()]
            dap_apps = [a for a in apps if "dap" in a.get("fertilizerName", "").lower()]

            if urea_apps:
                nutrient_tips.append(
                    f"Urea application of {urea_apps[0].get('quantity','recommended dose')} is planned. "
                    "Split applications and avoid applying before heavy rain to reduce N loss."
                )
            if dap_apps:
                nutrient_tips.append(
                    "You have planned DAP application. Avoid excessive DAP to prevent P buildup; balance with K and organic manure."
                )

            nutrient_tips.append(
                "Monitor leaf colour and growth; use periodic soil/leaf tests to refine future fertilizer plans."
            )
        else:
            nutrient_tips.append(
                "No fertilizer schedule recorded. Prepare a yearly nutrient plan with split applications of N, P, K and organic manures."
            )

        # ---------- PEST & DISEASE ----------
        if protection_log and protection_log.get("controlTaken"):
            protection_tips.append(
                f"Pest/disease issue logged: {protection_log.get('pestDiseaseName','')}. "
                f"Control with {protection_log.get('controlDetails', {}).get('productName','recommended bio/chemical').title()} is recorded. "
                "Continue regular scouting and use IPM: clean cultivation, traps, and resistant varieties where possible."
            )
        else:
            protection_tips.append(
                "No crop protection record found. Inspect palms regularly for pests/diseases and keep records of any sprays or biocontrols used."
            )

        # ---------- HARVEST & MARKETING ----------
        if harvest_log:
            yield_qty = harvest_log.get("yieldQuantity")
            yield_unit = harvest_log.get("yieldUnit", "")
            grade = harvest_log.get("grade", "")
            marketing_tips.append(
                f"You harvested about {yield_qty} {yield_unit} of grade {grade}. "
                "Compare yield with local benchmarks; if lower, review water, nutrient and pest management in earlier stages."
            )
        if marketing_log:
            price = marketing_log.get("pricePerUnit")
            buyer = marketing_log.get("buyer", "")
            marketing_tips.append(
                f"Recorded sale to {buyer} at ₹{price} per {marketing_log.get('quantityUnit','unit')}. "
                "Compare prices across local markets and FPOs; explore storage or staggered sales to get better price."
            )

        return {
            "cropName": crop_name,
            "cropManagement": crop_management_tips,
            "nutrientManagement": nutrient_tips,
            "waterManagement": water_tips,
            "protectionManagement": protection_tips,
            "harvestMarketing": marketing_tips,
        }
