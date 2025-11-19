import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle
import sys

input_csv = sys.argv[sys.argv.index("--data") + 1]
save_path = sys.argv[sys.argv.index("--output") + 1]

df = pd.read_csv(input_csv)

X = df[["commit_size", "tests_failed"]]
y = df["build_time"]

model = RandomForestRegressor()
model.fit(X, y)

with open(save_path, "wb") as f:
    pickle.dump(model, f)

print("New model saved:", save_path)
