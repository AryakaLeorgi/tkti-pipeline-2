import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

csv_path = "ml/pipeline_metrics.csv"

print("Loading CSV from:", os.path.abspath(csv_path))

# FIX BOM + trim whitespace
df = pd.read_csv(csv_path, encoding="utf-8-sig")
df.columns = df.columns.str.strip()

print("Columns in CSV:", df.columns)

# Create label
if "result" not in df.columns:
    raise ValueError("ERROR: CSV missing 'result' column. Columns found: " + str(df.columns))

df["Success"] = df["result"].apply(lambda x: 1 if x == "SUCCESS" else 0)

X = df[["build_time", "test_time", "deploy_time"]]
y = df["Success"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "ml/model.pkl")

print("Model trained and saved.")
