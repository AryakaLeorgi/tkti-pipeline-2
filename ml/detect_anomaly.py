import joblib
import numpy as np
import sys

build = float(sys.argv[1])
test = float(sys.argv[2])
deploy = float(sys.argv[3])

model = joblib.load("ml/anomaly_model.pkl")

X = np.array([[build, test, deploy]])

pred = model.predict(X)

print("\n=== ANOMALY DETECTION RESULT ===")
print(f"Build: {build}, Test: {test}, Deploy: {deploy}")

if pred[0] == -1:
    print("Status: 🚨 ANOMALY DETECTED")
else:
    print("Status: Normal")
