import pandas as pd
import numpy as np
import sys

CSV_PATH = "data/pipeline_metrics.csv"

def load_training_stats():
    df = pd.read_csv(CSV_PATH)

    # Pakai nama kolom baru
    required_cols = ["BuildTime", "TestTime", "DeployTime"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing column in CSV: {col}")

    means = df[required_cols].mean()
    stds = df[required_cols].std()

    return means, stds

def detect_anomaly(build, test, deploy, means, stds):
    z_build = abs((build - means["BuildTime"]) / stds["BuildTime"])
    z_test = abs((test - means["TestTime"]) / stds["TestTime"])
    z_deploy = abs((deploy - means["DeployTime"]) / stds["DeployTime"])

    detail = []
    is_anomaly = False

    if z_build > 2:
        is_anomaly = True
        detail.append(f"BuildTime too high (z={z_build:.2f})")

    if z_test > 2:
        is_anomaly = True
        detail.append(f"TestTime too high (z={z_test:.2f})")

    if z_deploy > 2:
        is_anomaly = True
        detail.append(f"DeployTime too high (z={z_deploy:.2f})")

    return is_anomaly, detail

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 detect_anomaly.py <BuildTime> <TestTime> <DeployTime>")
        sys.exit(1)

    build = float(sys.argv[1])
    test = float(sys.argv[2])
    deploy = float(sys.argv[3])

    means, stds = load_training_stats()
    is_anomaly, reasons = detect_anomaly(build, test, deploy, means, stds)

    print("\n=== ANOMALY DETECTION RESULT ===")
    print(f"Build: {build}, Test: {test}, Deploy: {deploy}")

    if is_anomaly:
        print("Status: ANOMALY DETECTED")
        print("Reasons:")
        for r in reasons:
            print(f" - {r}")
    else:
        print("Status: Normal")

if __name__ == "__main__":
    main()
