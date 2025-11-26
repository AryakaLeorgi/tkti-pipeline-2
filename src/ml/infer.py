# src/ml/infer.py

from ml.utils import tokenize_to_vector, graph_features_to_vector
import joblib
import os
import numpy as np

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "model")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")


def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


def infer(graph, features, description):
    """
    Combine:
    - graph features (dict)
    - ML features vector
    - text description
    Then run ML prediction.
    """

    model = load_model()
    if model is None:
        raise RuntimeError(f"Model not found at: {MODEL_PATH}")

    # convert every part into numeric vectors
    text_vec = tokenize_to_vector(description)
    graph_vec = graph_features_to_vector(graph)

    # 'features' is already a numeric vector from your parser
    features_vec = features if isinstance(features, list) else []

    # combine all into single ML vector
    full_vector = np.array(graph_vec + features_vec + text_vec).reshape(1, -1)

    # run prediction
    prediction = model.predict(full_vector)[0]

    return prediction
