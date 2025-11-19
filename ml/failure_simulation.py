import sys
import random
import time
from datetime import datetime

def simulate_stage(stage):
    start = time.time()

    # chance of failure
    fail_chance = {
        "build": 0.15,
        "test": 0.20,
        "deploy": 0.10
    }.get(stage, 0.10)

    # simulate real stage time (1–3 seconds)
    duration = round(random.uniform(1.0, 3.0), 3)

    # simulate work
    time.sleep(duration)

    # randomly fail
    failed = random.random() < fail_chance

    # write log file
    log_file = f"{stage}.log"
    with open(log_file, "w") as f:
        f.write(f"STAGE: {stage}\n")
        f.write(f"DURATION: {duration}\n")
        f.write(f"FAILED: {failed}\n")
        f.write(f"TIMESTAMP: {datetime.utcnow().isoformat()}\n")

    print(f"[SIMULATION] Stage: {stage}")
    print(f"Duration: {duration}s")
    print("[FAILED]" if failed else "[OK] Stage completed normally")

    # return exit code for Jenkins
    if failed:
        sys.exit(1)

if __name__ == "__main__":
    stage = sys.argv[1]
    simulate_stage(stage)
