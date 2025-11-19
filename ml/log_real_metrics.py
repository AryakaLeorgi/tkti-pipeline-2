import os
import csv
from datetime import datetime

OUT_PATH = "data/real_pipeline_metrics.csv"

def read_env_var(name, default="0"):
    return float(os.getenv(name, default))

def main():
    metrics = {
        "timestamp": datetime.utcnow().isoformat(),
        "build_time": read_env_var("BUILD_TIME"),
        "test_time": read_env_var("TEST_TIME"),
        "deploy_time": read_env_var("DEPLOY_TIME"),
        "result": os.getenv("PIPELINE_RESULT", "UNKNOWN"),
    }

    write_header = not os.path.exists(OUT_PATH)

    with open(OUT_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=metrics.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(metrics)

    print("Saved real CI/CD metrics:", metrics)

if __name__ == "__main__":
    main()
