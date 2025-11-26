import csv
import random

OUT = "data/simulated_large_ci_dataset.csv"
N = 2000  # jumlah sample

def generate_row():
    build = abs(random.gauss(90, 25))
    test = abs(random.gauss(45, 15))
    deploy = abs(random.gauss(20, 7))
    lines_changed = abs(int(random.gauss(300, 140)))
    files_changed = max(1, int(lines_changed / random.randint(20, 50)))
    weekend = random.random() < 0.15
    developer_exp = random.choice(["junior", "mid", "senior"])

    # label
    success = 1
    if build > 160 or test > 120 or "junior" in developer_exp and random.random() < 0.2:
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
