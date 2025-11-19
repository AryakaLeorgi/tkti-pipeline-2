import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load simulated dataset
df = pd.read_csv("pipeline_metrics.csv")

# Fill missing failure reasons
df["FailureReason"] = df["FailureReason"].fillna("None")

# Features and target
X = df[["BuildTime", "TestTime", "DeployTime"]]
y = df["Success"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Print report
print(classification_report(y_test, y_pred))

# Save model
joblib.dump(model, "ci_cd_model.pkl")
print("✅ Model saved as ci_cd_model.pkl")
