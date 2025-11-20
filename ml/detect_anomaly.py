import pandas as pd
import sys

CSV_PATH = "pipeline_metrics.csv"
df = pd.read_csv(CSV_PATH)

# ====== 1. Detect candidate numeric columns ======
numeric_cols = [
    c for c in df.columns
    if df[c].dtype in ["float64", "int64"]
]

# ====== 2. Filter out binary/fake metric columns ======
exclude_keywords = ["success", "status", "result", "pass", "fail"]

filtered_cols = []
for col in numeric_cols:
    lower = col.lower()

    # exclude obvious columns
    if any(k in lower for k in exclude_keywords):
        continue

    # exclude binary values (0/1 or True/False)
    unique_vals = df[col].dropna().unique()
    if len(unique_vals) <= 2:   # binary
        continue

    filtered_cols.append(col)

if len(filtered_cols) == 0:
    raise ValueError("Tidak ada kolom durasi numerik yang valid ditemukan!")

print(f"[INFO] Menggunakan kolom untuk anomaly detection: {filtered_cols}")

# ====== 3. Mean values ======
train_means = df[filtered_cols].mean()

# ====== 4. Input validation ======
if len(sys.argv) - 1 != len(filtered_cols):
    raise ValueError(
        f"Jumlah input salah! Anda memberikan {len(sys.argv)-1}, "
        f"namun model membutuhkan {len(filtered_cols)} input: {filtered_cols}"
    )

incoming_values = list(map(float, sys.argv[1:]))
incoming = dict(zip(filtered_cols, incoming_values))

# ====== 5. Compute deviation ======
diffs = {}
THRESHOLD = 2.0

for col in filtered_cols:
    mean_val = train_means[col]
    new_val = incoming[col]

    deviation = 0 if mean_val == 0 else abs(new_val - mean_val) / mean_val
    diffs[col] = deviation

# ====== 6. Result ======
max_col = max(diffs, key=diffs.get)
max_dev = diffs[max_col]
is_anomaly = max_dev > THRESHOLD

print("---- ANOMALY CHECK ----")
for c, d in diffs.items():
    print(f"{c}: deviation = {d*100:.2f}%")

if is_anomaly:
    print("\n⚠️ ANOMALY DETECTED")
    print(f"Stage '{max_col}' terlalu lambat dibanding dataset training.")
else:
    print("\n✅ NORMAL — Tidak ada anomaly.")
