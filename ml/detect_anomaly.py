import joblib
import numpy as np
import warnings

# Matikan warning sklearn
warnings.filterwarnings("ignore", category=UserWarning)

# Load model
model = joblib.load("ml/model.pkl")

def get_pipeline_input():
    """Coba baca input pipeline."""
    import sys
    data = sys.argv[1:]  # Argument CLI
    if len(data) == 3:
        try:
            return [float(x) for x in data]
        except:
            return None
    return None

# Coba ambil input
features = get_pipeline_input()

if features is None:
    print("[WARNING]")
    features = np.random.uniform(1.5, 5.0, size=3).round(3).tolist()

print(f"[INFO] Anomaly Input: {features}")

# Model expect array shape (1,3)
X = np.array(features).reshape(1, -1)

# Prediction
prediction = model.predict(X)[0]
score = model.predict_proba(X)[0][1]

is_anomaly = prediction == 1

print("\n=== ANOMALY RESULT ===")
print(f"Prediction: {'ANOMALY' if is_anomaly else 'NORMAL'}")
print(f"Score: {score:.4f}")
print(f"ANOMALY_FLAG={str(is_anomaly).lower()}")
