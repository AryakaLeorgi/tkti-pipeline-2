import os
import json
import joblib
import numpy as np

ERROR_DIR = "ci/generated_errors"


def load_model():
    return joblib.load("ml/model.pkl")


def load_latest_error():
    files = sorted(
        [f for f in os.listdir(ERROR_DIR) if f.endswith(".json")],
        reverse=True
    )
    if not files:
        return None

    with open(os.path.join(ERROR_DIR, files[0]), "r") as f:
        return json.load(f)


def to_feature_vector(err):
    return np.array([
        err["build_time"],
        err["test_fail_rate"],
        err["cpu_load"]
    ]).reshape(1, -1)


def detect():
    model = load_model()
    err = load_latest_error()

    if not err:
        print("NO ERROR DATA FOUND.")
        return

    features = to_feature_vector(err)
    pred = model.predict(features)[0]
    prob = model.predict_proba(features)[0]

    print("=== MODEL ANOMALY DIAGNOSIS ===")
    print(f"Error type        : {err['type']}")
    print(f"Message           : {err['message']}")
    print(f"Predicted anomaly : {pred}")
    print(f"Confidence        : {prob[pred]:.3f}")
    print("=== RAW FEATURES ===")
    print(err)


if __name__ == "__main__":
    detect()
