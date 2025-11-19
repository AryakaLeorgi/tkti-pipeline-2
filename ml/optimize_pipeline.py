import pandas as pd
import joblib

df = pd.read_csv('pipeline_metrics.csv').tail(1)
model = joblib.load('ci_cd_model.pkl')

prediction = model.predict(df[['BuildTime', 'TestTime', 'DeployTime']])
print("Predicted Success:", prediction)

# Simple advice
if df["BuildTime"].iloc[0] > 4:
    print("⚠ Build terlalu lama → Optimize caching.")
if df["TestTime"].iloc[0] > 3:
    print("⚠ Test terlalu lama → Gunakan parallel testing.")
if df["DeployTime"].iloc[0] > 2:
    print("⚠ Deploy terlalu lama → Gunakan lightweight artifact.")
