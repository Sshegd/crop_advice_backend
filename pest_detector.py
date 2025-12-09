from pest_db import PEST_DB
import datetime

class PestDetector:

    def detect(self, crop_name, weather, stage, symptoms_text=None):
        crop = crop_name.lower()

        if crop not in PEST_DB:
            return []

        month_name = datetime.datetime.now().strftime("%B")

        alerts = []

        for pest, rules in PEST_DB[crop].items():
            match = True

            # Rule: temp greater than X
            if "temp_gt" in rules:
                if not (weather["temp"] > rules["temp_gt"]):
                    match = False

            # Rule: humidity greater
            if "humidity_gt" in rules:
                if not (weather["humidity"] > rules["humidity_gt"]):
                    match = False

            # Rule: humidity lesser
            if "humidity_lt" in rules:
                if not (weather["humidity"] < rules["humidity_lt"]):
                    match = False

            # Rule: rainfall greater
            if "rainfall_gt" in rules:
                if not (weather["rainfall"] > rules["rainfall_gt"]):
                    match = False

            # Rule: rainfall lesser
            if "rainfall_lt" in rules:
                if not (weather["rainfall"] < rules["rainfall_lt"]):
                    match = False

            # Rule: temperature in range
            if "temp_range" in rules:
                lo, hi = rules["temp_range"]
                if not (lo <= weather["temp"] <= hi):
                    match = False

            # Stage match
            if "stage" in rules:
                if stage not in rules["stage"]:
                    match = False

            # Month match
            if "season" in rules:
                if month_name not in rules["season"]:
                    match = False

            # Symptom text matching
            if symptoms_text:
                if rules["symptoms"].split(" ")[0].lower() not in symptoms_text.lower():
                    pass  # soft check (not blocking)

            if match:
                alerts.append({
                    "pest": pest,
                    "symptoms": rules["symptoms"],
                    "preventive": rules["preventive"],
                    "corrective": rules["corrective"]
                })

        return alerts
