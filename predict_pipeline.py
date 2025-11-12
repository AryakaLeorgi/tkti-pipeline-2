# predict_pipeline.py
import argparse
import joblib
import pandas as pd
import sys

# --- Parse CLI arguments ---
parser = argparse.ArgumentParser()
parser.add_argument("--buildTime", type=float, required=True)
parser.add_argument("--testTime", type=float, required=True)
parser.add_argument("--deployTime", type=float, required=True)
parser.add_argument("--failureReason", type=str, default="None")
args = parser.parse_args()

# --- Load trained model ---
model = joblib.load("pipeline_success_model.pkl")

# --- Prepare input ---
failure_reason_options = [
    "None", "UnitTestError", "IntegrationFail", "Timeout", "BuildScriptError"
]

# One-hot encode the failure reason
data = {f"FailureReason_{reason}": 0 for reason in failure_reason_options[1:]}  # skip 'None'
if args.failureReason in data:
    data[f"FailureReason_{args.failureReason}"] = 1

# Add numerical features
data["BuildTime"] = args.buildTime
data["TestTime"] = args.testTime
data["DeployTime"] = args.deployTime

# --- Make prediction ---
df = pd.DataFrame([data])
pred = model.predict(df)[0]
prob = model.predict_proba(df)[0][1]

# --- Output ---
if pred == 1:
    print(f"✅ Prediction: SUCCESS ({prob*100:.2f}% confidence)")
else:
    print(f"❌ Prediction: FAILURE ({prob*100:.2f}% confidence)")

# Exit code 0 (success) or 1 (predicted fail)
sys.exit(0 if pred == 1 else 1)
