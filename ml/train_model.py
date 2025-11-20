import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

CSV_PATH = "data/pipeline_metrics.csv"
MODEL_PATH = "ml/model.pkl"

def load_data():
    print(f"Loading CSV from: {CSV_PATH}")

    df = pd.read_csv(CSV_PATH)

    # Pastikan kolom ada
    required_cols = ["BuildTime", "TestTime", "DeployTime", "Success", "FailureReason"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"CSV missing column: {col}")

    return df

def preprocess(df):
    # Success sudah 1/0 → aman
    df["Success"] = df["Success"].astype(int)

    # Encode FailureReason (categorical)
    df["FailureReason"] = df["FailureReason"].fillna("None")
    df["FailureReasonEncoded"] = df["FailureReason"].astype("category").cat.codes

    features = df[["BuildTime", "TestTime", "DeployTime", "FailureReasonEncoded"]]
    labels = df["Success"]

    return features, labels, df

def train(features, labels):
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.25, random_state=42
    )

    model = RandomForestClassifier(n_estimators=120, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    print("\n=== MODEL TRAINED ===")
    print("Accuracy:", acc)
    print(classification_report(y_test, preds))

    return model

def save_model(model):
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")

def main():
    df = load_data()
    features, labels, df = preprocess(df)
    model = train(features, labels)
    save_model(model)

if __name__ == "__main__":
    main()
