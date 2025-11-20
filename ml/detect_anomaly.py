import sys
import joblib
import numpy as np
import pandas as pd

REQUIRED_COLUMNS = ['BuildTime', 'TestTime', 'DeployTime']

# Jika argumen kosong → generate random data
if len(sys.argv) == 1:
    print("[WARNING] Tidak ada input dari pipeline — menggunakan random data untuk anomaly check.")
    build = round(np.random.uniform(1.0, 5.0), 3)
    test = round(np.random.uniform(1.0, 5.0), 3)
    deploy = round(np.random.uniform(1.0, 5.0), 3)
    values = [build, test, deploy]
else:
    # Input harus 3 angka
    values = list(map(float, sys.argv[1:]))
    if len(values) != 3:
        raise ValueError(
            f"Jumlah input salah! Anda memberikan {len(values)}, "
            f"namun model membutuhkan 3 input: {REQUIRED_COLUMNS}"
        )

print(f"[INFO] Anomaly Input: {values}")

# Load model
model = joblib.load("ml/model.pkl")

# Convert to dataframe
df = pd.DataFrame([values], columns=REQUIRED_COLUMNS)

# Predict anomaly
prediction = model.predict(df)[0]
score = model.predict_proba(df)[0][1]

print("\n=== ANOMALY RESULT ===")
print(f"Prediction: {'ANOMALY' if prediction == 1 else 'NORMAL'}")
print(f"Score: {score:.4f}")
