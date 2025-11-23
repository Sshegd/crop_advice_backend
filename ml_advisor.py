# ml_advisor.py
import os
from typing import List, Tuple, Dict, Any

import numpy as np
import joblib


class MLAdvisor:
    def __init__(self):
        self.existing_model = None
        self.new_crop_model = None

        # Load existing-crop model
        try:
            path_existing = os.path.join("models", "existing_model.pkl")
            if os.path.exists(path_existing):
                self.existing_model = joblib.load(path_existing)
                print("[MLAdvisor] Loaded existing_model.pkl")
            else:
                print("[MLAdvisor] existing_model.pkl not found – using fallback logic.")
        except Exception as e:
            print("[MLAdvisor] Error loading existing_model.pkl:", e)

        # Load new-crop model
        try:
            path_new = os.path.join("models", "new_crop_model.pkl")
            if os.path.exists(path_new):
                self.new_crop_model = joblib.load(path_new)
                print("[MLAdvisor] Loaded new_crop_model.pkl")
            else:
                print("[MLAdvisor] new_crop_model.pkl not found – using fallback logic.")
        except Exception as e:
            print("[MLAdvisor] Error loading new_crop_model.pkl:", e)

    # For /health endpoint
    def models_loaded(self) -> Dict[str, bool]:
        return {
            "existing_model": self.existing_model is not None,
            "new_crop_model": self.new_crop_model is not None,
        }

    # ---------- EXISTING CROP ADVICE ---------- #
    def existing_crop_advice(
        self,
        crop_name: str,
        stage: str,
        logs: List[Dict[str, Any]]
    ) -> Tuple[str, List[str]]:
        """
        Use ML model if available, else simple heuristic based on logs.
        """

        # ====== 1. FEATURE ENGINEERING (example) ======
        # You MUST align this with how you trained your model.
        # For now, we use very simple features:
        n_logs = len(logs)
        n_irrigations = sum(1 for l in logs if l.get("subActivity") == "water_management")
        n_fertilizer = sum(1 for l in logs if l.get("subActivity") == "nutrient_management")

        X = np.array([[n_logs, n_irrigations, n_fertilizer]], dtype=float)

        # ====== 2. ML INFERENCE (if model exists) ======
        if self.existing_model is not None:
            try:
                # Suppose model.predict_proba returns risk score
                risk_prob = self.existing_model.predict_proba(X)[0, 1]
                risk_level = "high" if risk_prob > 0.7 else "medium" if risk_prob > 0.4 else "low"

                base = (
                    f"For {crop_name} at {stage} stage, the ML model predicts "
                    f"{risk_level} risk based on {n_logs} recorded activities."
                )
                recs = []

                if risk_level == "high":
                    recs.append("Increase field monitoring and consider additional pest scouting.")
                    recs.append("Verify fertilizer and irrigation schedule match local recommendations.")
                elif risk_level == "medium":
                    recs.append("Maintain current practices but closely watch for pest/disease symptoms.")
                else:
                    recs.append("Your management looks good; continue logging activities regularly.")

                return base, recs

            except Exception as e:
                print("[MLAdvisor] Error in existing_model prediction:", e)

        # ====== 3. FALLBACK HEURISTIC ======
        base = (
            f"For {crop_name} at {stage} stage, the system found {n_logs} activity records. "
            "More detailed logs will improve advisory quality in future."
        )
        recs = []

        if n_irrigations == 0:
            recs.append("No irrigation logs found. Ensure the crop is receiving adequate water.")
        else:
            recs.append(f"Irrigation recorded {n_irrigations} time(s). Keep frequency consistent.")

        if n_fertilizer == 0:
            recs.append("No fertilizer applications logged. Check nutrient schedule for this crop.")
        else:
            recs.append(f"Fertilizer applications logged {n_fertilizer} time(s). Review doses and intervals.")

        recs.append("Try to fill sowing, water, nutrient, and pest logs soon after each operation.")

        return base, recs

    # ---------- NEW CROP RECOMMENDATION ---------- #
    def new_crop_recommend(
        self,
        features: Dict[str, Any]
    ) -> Tuple[str, List[str], str]:
        """
        features: dict with keys like soilType, area, district, weather, etc.
        Returns: (base_advisory, recommendations_list, best_crop_name)
        """

        soil = (features.get("soilType") or "").lower()
        area = features.get("area", "")
        district = features.get("district", "")
        weather = features.get("weather", {})

        # ====== 1. FEATURE VECTOR (example only) ======
        # You must mirror your training preprocessing here.
        # We'll just turn some categorical things into dummy numbers
        # to keep code valid even if the model is missing.
        soil_code = 0
        if "red" in soil:
            soil_code = 1
        elif "black" in soil:
            soil_code = 2
        elif "laterite" in soil:
            soil_code = 3

        X = np.array([[soil_code]], dtype=float)  # placeholder

        best_crop = "areca nut"  # default suggestion

        # ====== 2. ML INFERENCE (if model exists) ======
        if self.new_crop_model is not None:
            try:
                # example: model.predict returns an index or crop name
                pred = self.new_crop_model.predict(X)[0]
                best_crop = str(pred)
            except Exception as e:
                print("[MLAdvisor] Error in new_crop_model prediction:", e)

        # ====== 3. BUILD ADVISORY TEXT ======
        base = (
            f"For your farm in {district} with {area} and {soil} soil, "
            f"{best_crop} is a suitable crop for good yield and profitability, "
            "according to the current model and available data."
        )

        recs = [
            f"Use certified, high-quality planting material for {best_crop}.",
            "Plan irrigation schedule considering local rainfall and soil water-holding capacity.",
            "Follow recommended fertilizer doses split into multiple applications across the season.",
            "Adopt integrated pest management (IPM): regular scouting, traps, and need-based sprays.",
            "Keep recording all operations in the digital farm diary to refine future advisories."
        ]

        return base, recs, best_crop
