import joblib
import numpy as np
import sys
import random

MODEL_PATH = "ml/model.pkl"

def load_model():
    return joblib.load(MODEL_PATH)

def generate_random_input():
    return [
        round(random.uniform(0.5, 5.0), 3),  # BuildTime
        round(random.uniform(0.5, 5.0), 3),  # TestTime
        round(random.uniform(0.5, 5.0), 3)   # DeployTime
    ]

if __name__ == "__main__":
    model = load_model()

    # Ambil input dari argumen pipeline
    if len(sys.argv) == 4:
        try:
            bt = float(sys.argv[1])
            tt = float(sys.argv[2])
            dt = float(sys.argv[3])
            features = [bt, tt, dt]
        except ValueError:
            print("[ERROR] Input harus berupa angka.")
            exit(1)
    else:
        print("[WARNING] Tidak ada input dari pipeline — menggunakan random data untuk anomaly check.")
        features = generate_random_input()

    print(f"[INFO] Anomaly Input: {features}")

    arr = np.array([features])
    prediction = model.predict(arr)[0]
    score = model.predict_proba(arr)[0][1]

    print("\n=== ANOMALY RESULT ===")
    print("Prediction:", "ANOMALY" if prediction == 1 else "NORMAL")
    print(f"Score: {score:.4f}")

    # === OUTPUT FLAG FOR JENKINS ===
    if prediction == 1:
        print("ANOMALY_FLAG=true")
    else:
        print("ANOMALY_FLAG=false")
