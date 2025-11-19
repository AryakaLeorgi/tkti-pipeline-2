import sys
import pandas as pd
import joblib

model = joblib.load("models/pipeline_model.pkl")

build = float(sys.argv[1])
test = float(sys.argv[2])
deploy = float(sys.argv[3])

X = pd.DataFrame([[build, test, deploy]], 
    columns=["build_time", "test_time", "deploy_time"])

prob = model.predict_proba(X)[0][1]

print(f"Failure risk: {prob}")

if prob > 0.7:
    print("ANOMALY DETECTED: High failure probability!")
    sys.exit(1)
