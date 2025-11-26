import numpy as np

class AnomalyEngine:
    def detect(self, values):
        if len(values) < 5:
            return False

        mean = np.mean(values)
        std = np.std(values)

        anomalies = [v for v in values if abs(v - mean) > 2 * std]

        return {
            "is_anomaly": len(anomalies) > 0,
            "count": len(anomalies),
            "threshold": float(mean + 2 * std)
        }
