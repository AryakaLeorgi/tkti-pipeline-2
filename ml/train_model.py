import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

CSV_PATH = "data/pipeline_metrics.csv"
MODEL_PATH = "ml/model.pkl"

def main():

    # ==========================
    # 1. CEK CSV EXIST
    # ==========================
    if not os.path.exists(CSV_PATH):
        print(f"[ERROR] CSV not found: {CSV_PATH}")
        print("Pastikan file pipeline_metrics.csv sudah ada di folder data/")
        return

    print("Loading CSV from:", CSV_PATH)

    # ==========================
    # 2. LOAD DATA
    # ==========================
    df = pd.read_csv(CSV_PATH)

    # Pastikan kolom sesuai format:
    # timestamp, build_time, test_time, deploy_time, result
    required_cols = ["build_time", "test_time", "deploy_time", "result"]
    for col in required_cols:
        if col not in df.columns:
            print(f"[ERROR] Kolom '{col}' tidak ditemukan di CSV!")
            return

    # Konversi label ke angka
    df["Success"] = df["result"].apply(lambda x: 1 if x == "SUCCESS" else 0)

    X = df[["build_time", "test_time", "deploy_time"]]
    y = df["Success"]

    # ==========================
    # 3. SPLIT DATA
    # ==========================
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ==========================
    # 4. TRAIN MODEL
    # ==========================
    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=8,
        random_state=42
    )

    model.fit(X_train, y_train)

    # ==========================
    # 5. EVALUASI
    # ==========================
    acc = model.score(X_test, y_test)
    print(f"Model accuracy: {acc:.4f}")

    # ==========================
    # 6. SIMPAN MODEL
    # ==========================
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
