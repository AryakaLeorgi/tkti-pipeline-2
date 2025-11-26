# src/ml/generate_dummy_model.py

import joblib
import os
from sklearn.dummy import DummyClassifier

MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")

def main():
    os.makedirs(MODEL_DIR, exist_ok=True)

    # A classifier that always predicts class "0"
    model = DummyClassifier(strategy="constant", constant=0)
    model.fit([[0], [1]], [0, 0])  # minimal required fit

    joblib.dump(model, MODEL_PATH)

    print(f"Dummy model created at: {MODEL_PATH}")

if __name__ == "__main__":
    main()
