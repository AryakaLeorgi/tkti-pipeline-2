import csv
import os
from datetime import datetime
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--build", type=float, required=True)
parser.add_argument("--test", type=float, required=True)
parser.add_argument("--deploy", type=float, required=True)
args = parser.parse_args()

OUT_PATH = "data/real_pipeline_metrics.csv"

os.makedirs("data", exist_ok=True)

file_exists = os.path.isfile(OUT_PATH)

with open(OUT_PATH, "a", newline="") as f:
    writer = csv.writer(f)

    if not file_exists:
        writer.writerow(["Timestamp", "BuildTime", "TestTime", "DeployTime"])

    writer.writerow([
        datetime.utcnow().isoformat(),
        args.build,
        args.test,
        args.deploy
    ])

print("Logged real pipeline metrics successfully.")
