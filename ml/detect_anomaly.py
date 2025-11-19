import pandas as pd
from sklearn.ensemble import IsolationForest

DATA = "data/real_pipeline_metrics.csv"

def main():
    df = pd.read_csv(DATA)

    model = IsolationForest(contamination=0.05)
    model.fit(df[["build_time","test_time","deploy_time"]])

    df["anomaly"] = model.predict(df[["build_time","test_time","deploy_time"]])

    risk = df["anomaly"].iloc[-1] == -1

    if risk:
        print("⚠ WARNING: anomaly detected in latest pipeline run")
    else:
        print("✓ No anomaly detected")

if __name__ == "__main__":
    main()
