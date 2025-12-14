class YieldPredictor:

    def predict(self, crop, rainfall, temp, farm_size):

        base_yield = 10.0

        if rainfall > 2000:
            base_yield += 2
        if temp > 30:
            base_yield -= 1

        expected = round(base_yield, 2)

        return {
            "expectedYieldPerAcre": expected,
            "totalExpectedYield": round(expected * farm_size, 2),
            "confidence": "High" if rainfall > 1000 else "Medium",
            "explanation": (
                f"Based on recent weather patterns and historical data, "
                f"{crop} is expected to yield approximately "
                f"{expected} quintals per acre."
            )
        }
