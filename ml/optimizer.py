import pandas as pd

df = pd.read_csv("pipeline_metrics.csv").tail(1).iloc[0]

build = df["BuildTime"]
test = df["TestTime"]

recommendation = ""

if build > 200:
    recommendation = "Kurangi waktu build (gunakan caching)"
elif test > 150:
    recommendation = "Kurangi waktu testing"
else:
    recommendation = "Pipeline sudah optimal"

with open("optimization_report.txt", "w") as f:
    f.write("Pipeline Optimization Report\n")
    f.write("=================================\n")
    f.write("Rekomendasi: " + recommendation)

print("⚠ " + recommendation)
