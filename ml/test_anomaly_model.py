import subprocess
import sys
import pandas as pd

CSV_PATH = "pipeline_metrics.csv"
df = pd.read_csv(CSV_PATH)

# Ambil kolom time otomatis dari detect_anomaly.py logic
numeric_cols = [c for c in df.columns if df[c].dtype in ["float64", "int64"]]
exclude_keywords = ["success", "status", "result", "pass", "fail"]

filtered_cols = []
for col in numeric_cols:
    lower = col.lower()
    if any(k in lower for k in exclude_keywords):
        continue
    unique_vals = df[col].dropna().unique()
    if len(unique_vals) <= 2:
        continue
    filtered_cols.append(col)

print(f"[INFO] Testing anomaly model with columns: {filtered_cols}")
means = df[filtered_cols].mean()

def run_case(values_dict, expect_anomaly: bool):
    """
    values_dict: {"BuildTime": 100, "TestTime": 200, "DeployTime": 50}
    expect_anomaly: True or False
    """
    cmd_args = [str(values_dict[col]) for col in filtered_cols]
    cmd = ["python3", "ml/detect_anomaly.py"] + cmd_args

    print(f"\n[TEST] Running case: {values_dict}")
    print(f"Expect anomaly: {expect_anomaly}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout + result.stderr

    print(output)

    detected = "ANOMALY DETECTED" in output

    if detected != expect_anomaly:
        print("❌ TEST FAILED")
        sys.exit(1)

    print("✅ TEST PASSED")


# ===============================
# NORMAL CASE (should NOT be anomaly)
# ===============================
normal_case = {col: means[col] for col in filtered_cols}
run_case(normal_case, expect_anomaly=False)

# ===============================
# EXTREME CASES
# ===============================
extreme_cases = [
    # Slow Build
    {col: (means[col] * (10 if "build" in col.lower() else 1)) for col in filtered_cols},

    # Slow Tests
    {col: (means[col] * (8 if "test" in col.lower() else 1)) for col in filtered_cols},

    # Slow Deploy
    {col: (means[col] * (12 if "deploy" in col.lower() else 1)) for col in filtered_cols},

    # All slow (chaos mode)
    {col: means[col] * 15 for col in filtered_cols},
]

for case in extreme_cases:
    run_case(case, expect_anomaly=True)

print("\n🎉 ALL ANOMALY MODEL TESTS PASSED — model is healthy.")
