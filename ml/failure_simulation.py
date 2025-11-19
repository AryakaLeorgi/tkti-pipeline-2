import sys
import random
import time

STAGE = sys.argv[1]
FAIL_RATE = 0.10  # 10% failure simulation

print(f"[SIMULATION] Stage: {STAGE}")

# simulate real work
time.sleep(random.uniform(0.5, 2.5))

# random failure
if random.random() < FAIL_RATE:
    print(f"[FAILURE] Simulated failure in stage: {STAGE}")
    sys.exit(1)

print(f"[OK] Stage completed normally")
