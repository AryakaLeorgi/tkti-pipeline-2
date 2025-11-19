import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

CSV_PATH = "data/pipeline_metrics.csv"
MODEL_PATH = "ml/model.pkl"

def ensure_csv_exists():
    """Ensure CSV file and folder exist, otherwise create them."""
    folder = os.path.dirname(CSV_PATH)
    os.makedirs(folder, exist_ok=True)

    if not os.path.exists(CSV_PATH):
        print("[INFO] CSV not found, creating new:", CSV_PATH)
        with open(CSV_PATH, "w") as f:
            f.write("timestamp,build_time,test_time,deploy_time,result\n")
        return False  # CSV empty → don't train
    return True


def load_dataset():
    """Load dataset safely; if file empty, skip training."""
    df = pd.read_csv(CSV_PATH)

    if df.empty or len(df) < 5:
        print("[WARNING] Not enough data to train model (need at least 5 rows).")
        return None

    # Convert SUCCESS/FAILED → 1/0
    df["Success"] = df["result"].apply(lambda x: 1 if str(x).strip() == "SUCCESS" else 0)

    X = df[["build_time", "test_time", "deploy_time"]]
    y = df["Success"]

    return X, y


def train():
    print("[INFO] Checking CSV...")

    if not ensure_csv_exists():
        print("[INFO] CSV created but empty → skipping training.")
        return

    dataset = load_dataset()
    if dataset is None:
        print("[INFO] No training performed due to insufficient data.")
        return

    X, y = dataset

    print("[INFO] Training RandomForest model...")
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    print("[INFO] Model trained & saved to:", MODEL_PATH)


if __name__ == "__main__":
    train()
