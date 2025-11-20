import sys
import random
import time
from datetime import datetime, UTC

if len(sys.argv) < 2:
    print("Usage: python3 failure_simulation.py <stage>")
    sys.exit(1)

stage = sys.argv[1]

duration = round(random.uniform(1.0, 3.0), 3)
failed = random.random() < 0.2  # 20% failure rate

print(f"[SIMULATION] Stage: {stage}")
print(f"Duration: {duration}s")

if failed:
    print("[FAILED]")
    # Tetap exit 1 agar terdeteksi sebagai gagal
    sys.exit(1)
else:
    print("[SUCCESS]")
    sys.exit(0)
