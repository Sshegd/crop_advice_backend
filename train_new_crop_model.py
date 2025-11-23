# train_new_crop_model.py
"""
Train ML model for NEW CROP advisory using the Kaggle Crop Recommendation dataset.

Steps:
1. Put Crop_recommendation.csv in: data/Crop_recommendation.csv
2. Install deps: pip install -r requirements.txt
3. Run: python train_new_crop_model.py
4. It will create new_crop_model.pkl in project root.
"""

import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# ------------- CONFIG -------------
DATA_PATH = os.path.join("data", "Crop_recommendation.csv")  # from Data-Driven project
MODEL_PATH = "new_crop_model.pkl"

FEATURE_COLS = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
TARGET_COL = "label"
# ----------------------------------


def main():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. "
            "Place Crop_recommendation.csv from the Data-Driven project into the data/ folder."
        )

    df = pd.read_csv(DATA_PATH)

    X = df[FEATURE_COLS]
    y = df[TARGET_COL]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipe = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "model",
                RandomForestClassifier(
                    n_estimators=300,
                    random_state=42,
                    class_weight="balanced",
                    n_jobs=-1,
                ),
            ),
        ]
    )

    pipe.fit(X_train, y_train)

    train_acc = pipe.score(X_train, y_train)
    test_acc = pipe.score(X_test, y_test)
    print(f"Train accuracy: {train_acc:.4f}")
    print(f"Test  accuracy: {test_acc:.4f}")

    joblib.dump(pipe, MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
