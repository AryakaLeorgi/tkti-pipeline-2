import joblib
import pandas as pd
import argparse

# --- Parse CLI arguments from Jenkins ---
parser = argparse.ArgumentParser()
parser.add_argument("--buildTime", type=float, required=True)
parser.add_argument("--testTime", type=float, required=True)
parser.add_argument("--deployTime", type=float, required=True)
parser.add_argument("--failureReason", type=str, required=True)
args = parser.parse_args()

# --- Load model + column metadata ---
model = joblib.load("pipeline_success_model3.pkl")
model_columns = joblib.load("model_columns.pkl")

# --- Build input ---
df = pd.DataFrame([{
    "BuildTime": args.buildTime,
    "TestTime": args.testTime,
    "DeployTime": args.deployTime,
    "FailureReason": args.failureReason
}])

# One-hot encode and align with training columns
df = pd.get_dummies(df, columns=["FailureReason"], drop_first=True)

for col in model_columns:
    if col not in df.columns:
        df[col] = 0  # fill missing columns

df = df[model_columns]  # ensure same order

# --- Predict ---
pred = model.predict(df)[0]
print(f"✅ Prediction result: {pred}")
