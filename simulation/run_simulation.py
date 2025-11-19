import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--output", default="pipeline_metrics.csv")
args = parser.parse_args()

records = []

for _ in range(1000):
    build = np.random.randint(10, 300)
    test = np.random.randint(5, 200)
    deploy = np.random.randint(1, 100)

    success = 1 if build < 200 and test < 150 else 0
    reason = "Slow Build" if build >= 200 else ("Slow Tests" if test >= 150 else "None")

    records.append([build, test, deploy, success, reason])

df = pd.DataFrame(records, columns=["BuildTime", "TestTime", "DeployTime", "Success", "FailureReason"])
df.to_csv(args.output, index=False)

print("✅ Generated", len(records), "simulation records.")
