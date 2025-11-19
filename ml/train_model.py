import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

df = pd.read_csv("pipeline_results.csv")

# Drop kolom reason untuk training (hanya training binary success)
df["FailureReason"] = df["FailureReason"].fillna("None")
X = df[["BuildTime", "TestTime", "DeployTime"]]
y = df["Success"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier()
model.fit(X_train, y_train)

print(classification_report(y_test, y_pred))

joblib.dump(model, "ci_cd_model.pkl")
