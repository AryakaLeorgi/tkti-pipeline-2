import pandas as pd
import numpy as np
import joblib
import os
import sys
import json

MODEL_PATH = "ml/model.pkl"

# Kolom yang digunakan model
FEATURE_COLS = ["BuildTime", "TestTime", "DeployTime", "FailureReasonEncoded"]

def load_model():
    if not os.path.exists(MODEL_PATH):
        print("[ERROR] Model not found! Run training first.")
        sys.exit(1)
    return joblib.load(MODEL_PATH)

def get_pipeline_inputs():
    """Ambil input dari Jenkins env variable kalau ada."""
    try:
        raw = os.getenv("PIPELINE_STAGE_TIMES")
        if raw:
            return json.loads(raw)
    except:
        pass

    return None


def detect(model, data_dict):
    """Convert dict → dataframe dengan nama kolom lengkap."""
    df = pd.DataFrame([{
        "BuildTime": data_dict.get("BuildTime", 0),
        "TestTime": data_dict.get("TestTime", 0),
        "DeployTime": data_dict.get("DeployTime", 0),
        "FailureReasonEncoded": data_dict.get("FailureReasonEncoded", 0),
    }])

    pred = model.predict(df)[0]
    prob = model.predict_proba(df)[0][pred]

    return pred, round(float(prob), 4), df


def main():
    model = load_model()

    inputs = get_pipeline_inputs()

    if inputs is None:
        print("[WARNING] No pipeline inputs — generating random case for detection.")
        inputs = {
            "BuildTime": round(np.random.uniform(0.5, 3.5), 3),
            "TestTime": round(np.random.uniform(0.5, 2.5), 3),
            "DeployTime": round(np.random.uniform(0.5, 2.0), 3),
            "FailureReasonEncoded": 0
        }

    pred, conf, df = detect(model, inputs)

    print("")
    print("=== ANOMALY DETECTION RESULT ===")
    print("Input:")
    print(df.to_string(index=False))
    print(f"\nPrediction: {'ANOMALY' if pred==1 else 'NORMAL'}")
    print(f"Confidence: {conf}")

    # Flag untuk Jenkins
    print(f"ANOMALY_FLAG={'true' if pred == 1 else 'false'}")


if __name__ == "__main__":
    main()
