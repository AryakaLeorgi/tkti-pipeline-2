# src/ml/utils.py

import re

def tokenize_to_vector(text):
    """
    Tokenize the text and convert tokens into simple numeric vector.
    This is a placeholder tokenizer — adjust as needed.
    """
    if text is None:
        return []

    # simple lowercase split tokenizer
    tokens = re.findall(r"\w+", text.lower())

    # convert each token to a simple hash-based ID
    vec = [hash(t) % 10000 for t in tokens]
    return vec


def graph_features_to_vector(features):
    """
    Convert graph features (dict) into a stable numeric vector.
    """
    if not isinstance(features, dict):
        return []

    # sort keys alphabetically for deterministic ordering
    keys = sorted(features.keys())
    return [features[k] for k in keys]
