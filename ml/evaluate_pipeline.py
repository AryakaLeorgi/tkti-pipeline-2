import pandas as pd
import joblib

df = pd.read_csv("pipeline_metrics.csv").tail(1)
model = joblib.load("ml/model.pkl")

X = df[["BuildTime", "TestTime", "DeployTime"]]
pred = model.predict(X)

print("Predicted Success:", pred)
