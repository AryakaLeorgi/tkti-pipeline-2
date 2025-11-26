import numpy as np
import re

def tokenize(text):
    tokens = re.findall(r"\w+", text.lower())
    vec = np.zeros(128)
    vec[: min(len(tokens), 128)] = np.arange(min(len(tokens), 128))
    return vec.tolist()

def graph_to_vector(features):
    return [
        features["target_count"],
        features["task_count"],
        int(features["uses_parallel"]),
        int(features["uses_junit"]),
        features["property_count"],
        len(features["javac_flags"]),
    ]

def tokenize_to_vector(text):
    # simple fallback tokenizer — customize as needed
    tokens = text.lower().split()
    return [hash(t) % 10000 for t in tokens]
