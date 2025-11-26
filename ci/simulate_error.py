import random
import json
import os

OUTPUT_DIR = "ci/generated_errors"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def simulate_error():
    """
    Generate a CI/CD anomaly case with higher frequency,
    more extreme conditions, and multi-cause failures.
    """

    # ==============================
    # BASE ERROR LIBRARY (banyak)
    # ==============================
    error_types = [

        # --- dependency issues ---
        {
            "type": "dependency_conflict",
            "build_time": random.randint(300, 900),
            "test_fail_rate": random.uniform(0.2, 0.5),
            "cpu_load": random.uniform(0.6, 0.85),
            "message": "Package version conflict detected between modules."
        },
        {
            "type": "dependency_resolve_timeout",
            "build_time": random.randint(400, 1200),
            "test_fail_rate": random.uniform(0.1, 0.3),
            "cpu_load": random.uniform(0.4, 0.7),
            "message": "Dependency resolver took too long — timed out."
        },

        # --- test anomalies ---
        {
            "type": "flaky_tests",
            "build_time": random.randint(50, 250),
            "test_fail_rate": random.uniform(0.4, 0.8),
            "cpu_load": random.uniform(0.3, 0.55),
            "message": "Test suite shows high nondeterminism (flakiness storm)."
        },
        {
            "type": "test_data_corruption",
            "build_time": random.randint(100, 250),
            "test_fail_rate": random.uniform(0.5, 0.9),
            "cpu_load": random.uniform(0.2, 0.4),
            "message": "Test input data corrupted — misaligned schemas."
        },

        # --- resource issues ---
        {
            "type": "cpu_exhaustion",
            "build_time": random.randint(500, 1500),
            "test_fail_rate": random.uniform(0.1, 0.3),
            "cpu_load": random.uniform(0.95, 1.0),
            "message": "CPU fully saturated — possible infinite loop or heavy job."
        },
        {
            "type": "ram_leak",
            "build_time": random.randint(300, 800),
            "test_fail_rate": random.uniform(0.2, 0.4),
            "cpu_load": random.uniform(0.7, 0.95),
            "message": "Memory leak detected in build process."
        },

        # --- network & artifact issues ---
        {
            "type": "network_timeout",
            "build_time": random.randint(200, 700),
            "test_fail_rate": random.uniform(0.0, 0.15),
            "cpu_load": random.uniform(0.2, 0.5),
            "message": "Network timeout while downloading artifacts."
        },
        {
            "type": "artifact_corruption",
            "build_time": random.randint(250, 800),
            "test_fail_rate": random.uniform(0.3, 0.6),
            "cpu_load": random.uniform(0.3, 0.5),
            "message": "Downloaded build artifact was corrupted."
        },

        # --- disk issues ---
        {
            "type": "disk_io_stall",
            "build_time": random.randint(600, 2000),
            "test_fail_rate": random.uniform(0.1, 0.25),
            "cpu_load": random.uniform(0.1, 0.3),
            "message": "Disk read/write slowdown — possible saturation."
        },
        {
            "type": "low_disk_space",
            "build_time": random.randint(300, 700),
            "test_fail_rate": random.uniform(0.1, 0.3),
            "cpu_load": random.uniform(0.3, 0.5),
            "message": "Insufficient disk space — build artifacts cannot be stored."
        },

        # --- corrupted metrics ---
        {
            "type": "metric_corruption",
            "build_time": random.uniform(-200, 2000),  # negative values included
            "test_fail_rate": random.uniform(-0.1, 1.5),
            "cpu_load": random.uniform(-0.5, 1.2),
            "message": "Monitoring system returned corrupted metrics."
        }
    ]

    # ===================================
    #     🔥 MULTI-ERROR COMBINATIONS
    # ===================================
    if random.random() < 0.25:  # 25% chance
        chosen = random.sample(error_types, k=2)

        return {
            "type": chosen[0]["type"] + "+ " + chosen[1]["type"],
            "build_time": max(chosen[0]["build_time"], chosen[1]["build_time"]),
            "test_fail_rate": min(1.0, (chosen[0]["test_fail_rate"] + chosen[1]["test_fail_rate"]) / 2),
            "cpu_load": max(chosen[0]["cpu_load"], chosen[1]["cpu_load"]),
            "message": f"Multiple anomalies detected:\n- {chosen[0]['message']}\n- {chosen[1]['message']}"
        }

    # ===================================
    #     🔥 CHAOS MODE ERRORS (10%)
    # ===================================
    if random.random() < 0.10:
        return {
            "type": "chaos_event",
            "build_time": random.uniform(1000, 5000),
            "test_fail_rate": random.uniform(0.7, 1.0),
            "cpu_load": random.uniform(0.9, 1.0),
            "message": "CHAOS MODE: random node failure, Docker daemon crash, or sudden infrastructure instability."
        }

    # ===================================
    #     NORMAL ERROR GENERATION
    # ===================================
    return random.choice(error_types)


def save_error(error_case):
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
