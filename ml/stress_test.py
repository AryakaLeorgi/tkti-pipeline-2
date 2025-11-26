import joblib
import pandas as pd
import numpy as np

MODEL_PATH = "ml/model.pkl"

print("[INFO] Loading model...")
model = joblib.load(MODEL_PATH)

print("[INFO] Running stress test...")

# Generate random 100 samples
data = pd.DataFrame({
    "BuildTime": np.random.uniform(0.5, 10, 100),
    "TestTime": np.random.uniform(0.5, 8, 100),
    "DeployTime": np.random.uniform(0.5, 5, 100),
})

preds = model.predict(data)

failures = (preds == 0).sum()
success = (preds == 1).sum()

print(f"Success: {success}, Failures: {failures}")

print("[DONE] Stress test completed.")
