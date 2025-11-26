import json
import numpy as np
from sklearn.svm import OneClassSVM
import re


def detect_anomaly(metrics_path="pipeline_metrics.json"):
    """
    Mendeteksi anomaly pada pipeline CI/CD berdasarkan:
    1. Threshold heuristik
    2. Pola error dari log
    3. ML anomaly scoring (One-Class SVM)
    """

    try:
        with open(metrics_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        return {
            "status": "error",
            "message": f"Metrics file {metrics_path} not found.",
            "anomaly": True,
            "severity": "high"
        }

    # -------------------------------
    # 1. Extract Metrics
    # -------------------------------
    build_time = data.get("build_time", None)
    test_failures = data.get("test_failures", 0)
    coverage = data.get("test_coverage", 100)
    log = data.get("last_logs", "")

    anomalies = []
    severity = "low"

    # --------------------------------
    # 2. Rule-based threshold detection
    # --------------------------------
    if build_time and build_time > 600:  # 10 minutes
        anomalies.append(f"Build time unusually high: {build_time}s")
        severity = "medium"

    if test_failures > 0:
        anomalies.append(f"There are {test_failures} test failures")
        severity = "medium"

    if coverage < 60:
        anomalies.append(f"Test coverage too low: {coverage}%")
        severity = "medium"

    # --------------------------------
    # 3. Log pattern detection
    # --------------------------------
    log_patterns = {
        "dependency": r"(dependency|version conflict|package not found)",
        "network": r"(timeout|connection refused|network unreachable)",
        "build": r"(compile error|syntax error|build failed)",
        "ml": r"(model mismatch|shape error|tensor|numpy)"
    }

    for name, pattern in log_patterns.items():
        if re.search(pattern, log, re.IGNORECASE):
            anomalies.append(f"Detected {name} related issue in logs")
            severity = "high"

    # --------------------------------
    # 4. ML-based anomaly scoring
    # --------------------------------
    # Vectorizing numeric metrics
    numeric_features = np.array([[ 
        build_time or 0,
        test_failures,
        coverage
    ]])

    # Normal/expected ranges for training (dummy)
    training_data = np.array([
        [200, 0, 90],
        [250, 1, 85],
        [300, 0, 92],
        [280, 0, 88],
        [260, 1, 87]
    ])

    clf = OneClassSVM(gamma="scale", nu=0.1)
    clf.fit(training_data)

    ml_pred = clf.predict(numeric_features)[0]  # -1 = anomaly

    if ml_pred == -1:
        anomalies.append("ML anomaly detector: unusual pipeline metrics detected")
        severity = "high"

    # --------------------------------
    # 5. Compile result
    # --------------------------------
    return {
        "status": "ok",
        "anomaly": len(anomalies) > 0,
        "severity": severity,
        "details": anomalies,
        "raw_metrics": data
    }
