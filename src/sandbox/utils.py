import json
import os

def load_metrics(path="/workspace/sandbox_output/metrics.json"):
    if not os.path.exists(path):
        return {}
    with open(path) as f:
        return json.load(f)
