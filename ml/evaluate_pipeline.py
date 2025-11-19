import pandas as pd
import json
import pickle
import sys

input_csv = sys.argv[sys.argv.index("--input") + 1]
model_path = sys.argv[sys.argv.index("--model") + 1]
output_path = sys.argv[sys.argv.index("--output") + 1]

df = pd.read_csv(input_csv)

# Load ML model
with open(model_path, "rb") as f:
    model = pickle.load(f)

prediction = model.predict(df)[0]

result = {
    "performance_score": float(prediction),
    "retrain_needed": prediction < 0.5  # threshold
}

with open(output_path, "w") as f:
    json.dump(result, f)

print("Evaluation saved:", output_path)
