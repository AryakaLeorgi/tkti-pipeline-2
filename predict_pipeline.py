import argparse
import pandas as pd
import joblib

# --- 1️⃣ Load arguments ---
parser = argparse.ArgumentParser()
parser.add_argument("--buildTime", type=float, required=True)
parser.add_argument("--testTime", type=float, required=True)
parser.add_argument("--deployTime", type=float, required=True)
parser.add_argument("--failureReason", type=str, required=True)
args = parser.parse_args()

# --- 2️⃣ Load model + column metadata ---
model = joblib.load("pipeline_success_model4.pkl")
model_columns = joblib.load("model_columns.pkl")

# --- 3️⃣ Prepare input data ---
data = pd.DataFrame([{
    "BuildTime": args.buildTime,
    "TestTime": args.testTime,
    "DeployTime": args.deployTime,
    "FailureReason_" + args.failureReason: 1
}])

# Add missing columns with 0 to align with training columns
for col in model_columns:
    if col not in data.columns:
        data[col] = 0
data = data[model_columns]

# --- 4️⃣ Predict ---
pred = model.predict(data)[0]
print(f"✅ Prediction result: {pred}")

# --- 5️⃣ Save result for Jenkins ---
with open("prediction_output.txt", "w") as f:
    f.write(f"Prediction result: {pred}\n")
