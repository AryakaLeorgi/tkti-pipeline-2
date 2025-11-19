import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load dataset
df = pd.read_csv("pipeline_metrics.csv")

# Konversi SUCCESS/FAIL → 1/0
df["Success"] = df["result"].apply(lambda x: 1 if x == "SUCCESS" else 0)

# Fitur
X = df[["build_time", "test_time", "deploy_time"]]
y = df["Success"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# Prediksi
y_pred = model.predict(X_test)

# Print evaluasi
print("=== Classification Report ===")
print(classification_report(y_test, y_pred))

# Save model ke file
joblib.dump(model, "ci_cd_model.pkl")
print("Model saved as ci_cd_model.pkl")
