import pandas as pd
import sys

# ====== 1. Load CSV ======
CSV_PATH = "pipeline_metrics.csv"
df = pd.read_csv(CSV_PATH)

# ====== 2. Detect duration columns automatically ======
# Ambil semua kolom float/int dan exclude non-metric seperti commit_id, status, timestamp, stage
numeric_cols = [
    c for c in df.columns
    if df[c].dtype in ["float64", "int64"]
]
if len(numeric_cols) == 0:
    raise ValueError(f"Tidak ada kolom numerik yang ditemukan dalam {CSV_PATH}")

print(f"[INFO] Menggunakan kolom untuk anomaly detection: {numeric_cols}")

# ====== 3. Compute mean from training CSV ======
train_means = df[numeric_cols].mean()

# ====== 4. Read CLI inputs ======
if len(sys.argv) - 1 != len(numeric_cols):
    raise ValueError(
        f"Jumlah input salah! Anda memberikan {len(sys.argv)-1}, "
        f"namun model membutuhkan {len(numeric_cols)} input: {numeric_cols}"
    )

incoming_values = list(map(float, sys.argv[1:]))

# Convert to dict: { "build_time": 1.2, "test_time": 0.9, ... }
incoming = dict(zip(numeric_cols, incoming_values))

# ====== 5. Compute anomaly score ======
diffs = {}
THRESHOLD = 2.0  # 200% deviasi = anomaly

for col in numeric_cols:
    mean_val = train_means[col]
    new_val = incoming[col]

    if mean_val == 0:
        deviation = 0
    else:
        deviation = abs(new_val - mean_val) / mean_val

    diffs[col] = deviation

# ====== 6. Determine anomaly ======
max_col = max(diffs, key=diffs.get)
max_dev = diffs[max_col]

is_anomaly = max_dev > THRESHOLD

# ====== 7. Print results ======
print("---- ANOMALY CHECK ----")
for c, d in diffs.items():
    print(f"{c}: deviation = {d*100:.2f}%")

if is_anomaly:
    print("\n⚠️ ANOMALY DETECTED")
    print(f"Stage '{max_col}' terlalu lambat dibanding data training.")
else:
    print("\n✅ NORMAL — Tidak ada anomaly.")
