import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

CSV_PATH = "data/pipeline_metrics.csv"
MODEL_PATH = "ml/model.pkl"

def load_data():
    print(f"Loading CSV from: {CSV_PATH}")
    df = pd.read_csv(CSV_PATH)

    required_cols = ["BuildTime", "TestTime", "DeployTime", "Success"]
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"CSV missing column: {col}")

    return df

def preprocess(df):
    df["Success"] = df["Success"].astype(int)

    FEATURES = ["BuildTime", "TestTime", "DeployTime"]
    X = df[FEATURES]
    y = df["Success"]

    return X, y, FEATURES

def train_multi_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=42
    )

    # ==============================
    # 📌 Candidate models
    # ==============================
    models = {
        "random_forest": RandomForestClassifier(n_estimators=120, random_state=42),
        "gradient_boosting": GradientBoostingClassifier(),
        "svm_rbf": SVC(kernel="rbf", probability=True),
        "logistic_regression": LogisticRegression(max_iter=500),
        "decision_tree": DecisionTreeClassifier()
    }

    scores = {}
    trained_models = {}

    print("\n=== TRAINING MULTIPLE MODELS ===")

    for name, model in models.items():
        print(f"\n➡️ Training: {name}")
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        acc = accuracy_score(y_test, preds)
        scores[name] = acc
        trained_models[name] = model

        print(f"Accuracy: {acc:.4f}")
        print(classification_report(y_test, preds))

    # ==============================
    # 📌 Pick best model
    # ==============================
    best_model_name = max(scores, key=scores.get)
    best_model = trained_models[best_model_name]

    print("\n=== RESULTS SUMMARY ===")
    for name, acc in scores.items():
        print(f"{name}: {acc:.4f}")

    print(f"\n🏆 Best model: {best_model_name} with accuracy {scores[best_model_name]:.4f}")

    return best_model

def save_model(model):
    joblib.dump(model, MODEL_PATH)
    print(f"\nModel saved to {MODEL_PATH}")

def main():
    df = load_data()
    X, y, features = preprocess(df)
    best_model = train_multi_model(X, y)
    save_model(best_model)

if __name__ == "__main__":
    main()
