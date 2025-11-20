import pandas as pd
from sklearn.ensemble import IsolationForest
import joblib

df = pd.read_csv("data/pipeline_metrics.csv")

X = df[["build_time", "test_time", "deploy_time"]]

model = IsolationForest(
    contamination=0.15,   # 15% dianggap anomaly (sangat sensitif)
    random_state=42
)

model.fit(X)

joblib.dump(model, "ml/anomaly_model.pkl")
print("Isolation Forest anomaly model saved.")
