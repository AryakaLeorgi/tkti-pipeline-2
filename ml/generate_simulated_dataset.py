import csv
import random

OUT = "data/simulated_large_ci_dataset.csv"
N = 2000  # jumlah sample

def generate_row():
    # --- NORMAL DISTRIBUTION ---
    build = abs(random.gauss(90, 25))
    test = abs(random.gauss(45, 15))
    deploy = abs(random.gauss(20, 7))
    lines_changed = abs(int(random.gauss(300, 140)))
    files_changed = max(1, int(lines_changed / random.randint(20, 50)))
    weekend = random.random() < 0.15
    developer_exp = random.choice(["junior", "mid", "senior"])

    # ============================================
    #       🔥 20–30% RANDOM ANOMALY INJECTION 🔥
    # ============================================
    if random.random() < 0.3:
        anomaly_type = random.choice([
            "extreme_build_spike",
            "extreme_test_spike",
            "deploy_stall",
            "massive_code_change",
            "negative_corrupted",
            "weird_zero_values",
            "cache_failure",
            "dependency_conflict",
            "flaky_test_storm"
        ])

        if anomaly_type == "extreme_build_spike":
            build = random.uniform(400, 3000)

        elif anomaly_type == "extreme_test_spike":
            test = random.uniform(200, 600)

        elif anomaly_type == "deploy_stall":
            deploy = random.uniform(80, 250)

        elif anomaly_type == "massive_code_change":
            lines_changed = random.randint(8000, 50000)
            files_changed = random.randint(200, 1500)

        elif anomaly_type == "negative_corrupted":
            # corrupt measurement
            build = random.uniform(-50, -1)
            test = random.uniform(-30, -1)

        elif anomaly_type == "weird_zero_values":
            build = 0
            test = 0
            deploy = 0

        elif anomaly_type == "cache_failure":
            build *= random.uniform(3, 10)

        elif anomaly_type == "dependency_conflict":
            test *= random.uniform(4, 12)

        elif anomaly_type == "flaky_test_storm":
            test = test + random.uniform(100, 400)

    # ============================================
    #              LABELING LOGIC
    # ============================================

    success = 1

    # strong failure conditions
    if build > 180 or test > 150 or deploy > 80:
        success = 0

    # weekend commits fail more often
    if weekend and random.random() < 0.35:
        success = 0

    # junior higher chance failure
    if developer_exp == "junior" and random.random() < 0.25:
        success = 0

    # corrupted data → always fail
    if build < 0 or test < 0:
        success = 0

    return [
        build, test, deploy, lines_changed,
        files_changed, int(weekend), developer_exp, success
    ]

header = [
    "build_time","test_time","deploy_time",
    "lines_changed","files_changed",
    "weekend_commit","developer_experience","success"
]

with open(OUT, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(header)
    for _ in range(N):
        w.writerow(generate_row())

print(f"Generated dataset: {OUT}")
