import random
import json
import os

OUTPUT_DIR = "ci/generated_errors"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def simulate_error():
    """
    Generate one synthetic pipeline anomaly case.
    Returns a dict describing the anomaly.
    """

    error_types = [
        {
            "type": "dependency_failure",
            "build_time": random.randint(200, 400),
            "test_fail_rate": random.uniform(0.1, 0.3),
            "cpu_load": random.uniform(0.6, 0.9),
            "message": "Dependency installation failed due to version conflict."
        },
        {
            "type": "test_flaky",
            "build_time": random.randint(50, 200),
            "test_fail_rate": random.uniform(0.3, 0.6),
            "cpu_load": random.uniform(0.3, 0.5),
            "message": "Unit tests show inconsistent output — flaky behaviour."
        },
        {
            "type": "resource_exhaustion",
            "build_time": random.randint(400, 700),
            "test_fail_rate": random.uniform(0.05, 0.2),
            "cpu_load": random.uniform(0.9, 1.0),
            "message": "CPU or RAM exhaustion detected."
        },
        {
            "type": "network_failure",
            "build_time": random.randint(150, 350),
            "test_fail_rate": random.uniform(0.0, 0.1),
            "cpu_load": random.uniform(0.2, 0.4),
            "message": "Network timeout during artifact download."
        }
    ]

    chosen = random.choice(error_types)
    return chosen


def save_error(error_case):
    """ Save to JSON for later ML training """
    filename = f"{OUTPUT_DIR}/error_{error_case['type']}_{random.randint(1000,9999)}.json"

    with open(filename, "w") as f:
        json.dump(error_case, f, indent=4)

    return filename


if __name__ == "__main__":
    err = simulate_error()

    if err:
        file = save_error(err)
        print(f"[OK] Simulated failure: {err['type']} → saved to {file}")
    else:
        print("[ERR] simulate_error() returned None")
