import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

CSV_PATH = "data/pipeline_metrics.csv"
MODEL_PATH = "ml/model.pkl"

def load_data():
    print(f"Loading CSV from: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)

    # Pastikan kolom ada
    required_cols = ["BuildTime", "TestTime", "DeployTime", "Success"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"CSV missing column: {col}")

    return df

def preprocess(df):
    df["Success"] = df["Success"].astype(int)  # target

    # ❌ REMOVE FailureReasonEncoded
    FEATURES = ["BuildTime", "TestTime", "DeployTime"]

    X = df[FEATURES]
    y = df["Success"]

    return X, y, FEATURES

def train(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    model = RandomForestClassifier(n_estimators=120, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    print("\n=== MODEL TRAINED ===")
    print("Accuracy:", accuracy_score(y_test, preds))
    print(classification_report(y_test, preds))

    return model

def save_model(model):
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")

def main():
    df = load_data()
    X, y, features = preprocess(df)
    model = train(X, y)
    save_model(model)

if __name__ == "__main__":
    main()
