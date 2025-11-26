import pandas as pd
import numpy as np
import os

os.makedirs("data", exist_ok=True)
OUT_PATH = "data/pipeline_metrics.csv"

N = 400  # jumlah data synthetic

np.random.seed(42)

def random_failure_reason():
    reasons = [
        "DependencyError",
        "UnitTestFailure",
        "Timeout",
        "ContainerBuildError",
        "DeploymentConfigError",
        "SecurityScanFail",
        "None"
    ]
    return np.random.choice(reasons)

rows = []

for i in range(N):
    build = np.random.uniform(1.0, 10.0)
    test = np.random.uniform(1.0, 10.0)
    deploy = np.random.uniform(1.0, 10.0)

    # tentukan failure pattern:
    if test > 7.5:
        reason = "UnitTestFailure"
        success = 0
    elif build > 8.5:
        reason = "DependencyError"
        success = 0
    elif deploy > 7.8:
        reason = "DeploymentConfigError"
        success = 0
    else:
        reason = "None"
        success = 1

    # random additional failure noise:
    if np.random.rand() < 0.1:
        success = 0
        reason = random_failure_reason()

    rows.append([build, test, deploy, success, reason])

df = pd.DataFrame(rows, columns=["BuildTime", "TestTime", "DeployTime", "Success", "FailureReason"])
df.to_csv(OUT_PATH, index=False)

print(f"[OK] Synthetic dataset created: {OUT_PATH} ({len(df)} rows)")
