import joblib
import pandas as pd
import json

model = joblib.load("ci_cd_model.pkl")

# contoh input pipeline REAL TIME  
new_run = pd.DataFrame([{
    "BuildTime": 120,
    "TestTime": 60,
    "DeployTime": 20
}])

pred = model.predict(new_run)[0]

decision = {
    "predicted_success": int(pred),
    "enable_cache": False,
    "skip_tests": False,
    "parallel_build": False
}

# RULE SIMPLE: ML-driven pipeline
if new_run["BuildTime"][0] > 100:
    decision["enable_cache"] = True

if new_run["TestTime"][0] > 80:
    decision["skip_tests"] = True

if new_run["BuildTime"][0] > 150:
    decision["parallel_build"] = True

with open("ml/decision.json", "w") as f:
    json.dump(decision, f, indent=4)

print("Generated ML decision:", decision)
