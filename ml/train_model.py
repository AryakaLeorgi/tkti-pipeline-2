import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

CSV = "pipeline_metrics.csv"

df = pd.read_csv(CSV)

# features
X = df[["build_time", "test_time", "deploy_time"]]
y = df["failed"]

model = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", RandomForestClassifier(n_estimators=200))
])

model.fit(X, y)
joblib.dump(model, "models/pipeline_model.pkl")

print("Model retrained and saved.")
