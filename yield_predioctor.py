# yield_predictor.py
import numpy as np
from sklearn.linear_model import LinearRegression

class YieldPredictor:
    def __init__(self):
        # Simple trained coefficients (can be replaced by real model)
        self.model = LinearRegression()
        X = np.array([
            [800, 28], [1000, 30], [1200, 32], [1500, 29]
        ])  # rainfall(mm), temperature(C)
        y = np.array([18, 22, 25, 27])  # quintal per acre
        self.model.fit(X, y)

    def predict(self, rainfall, temperature):
        pred = self.model.predict([[rainfall, temperature]])
        return round(float(pred[0]), 2)
