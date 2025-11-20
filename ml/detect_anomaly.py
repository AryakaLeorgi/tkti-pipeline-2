import sys
import joblib
import numpy as np
import os
import pandas as pd

MODEL_PATH = "ml/model.pkl"
CSV_PATH = "data/pipeline_metrics.csv"

# Load model
if not os.path.exists(MODEL_PATH):
    print("[ERROR] Model not found:", MODEL_PATH)
    sys.exit(1)

model = joblib.load(MODEL_PATH)

# Load training stats for explanation
df = pd.read_csv(CSV_PATH)

train_means = df[["build_time", "test_time", "deploy_time"]].mean()
train_stds = df[["build_time", "test_time", "deploy_time"]].std()

# Input values
build, test, deploy = map(float, sys.argv[1:4])
X = np.array([[build, test, deploy]])

prob = model.predict_proba(X)[0][1]

print(f"Prediction success probability: {prob:.4f}")

is_anomaly = prob < 0.5

# ---- Explanation Part ----
def z_score(val, mean, std):
    if std == 0:
        return 0
    return (val - mean) / std

z_build = z_score(build, train_means["build_time"], train_stds["build_time"])
z_test = z_score(test, train_means["test_time"], train_stds["test_time"])
z_deploy = z_score(deploy, train_means["deploy_time"], train_stds["deploy_time"])

# Collect explanations
explanations = []

if abs(z_build) > 2:
    explanations.append(f"Build time {build:.3f}s abnormal (z={z_build:.2f}).")

if abs(z_test) > 2:
    explanations.append(f"Test time {test:.3f}s abnormal (z={z_test:.2f}).")

if abs(z_deploy) > 2:
    explanations.append(f"Deploy time {deploy:.3f}s abnormal (z={z_deploy:.2f}).")

# Output
if is_anomaly:
    print("ANOMALY")
    print("Reason:")
    for e in explanations:
        print(" -", e)
else:
    print("NORMAL")
