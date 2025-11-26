import subprocess
import json
import time
import os

LOG_PATH = "/workspace/sandbox_output"

def ensure_dirs():
    os.makedirs(LOG_PATH, exist_ok=True)

def run_ant():
    start = time.time()
    proc = subprocess.Popen(
        ["ant", "-f", "build.xml"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = proc.communicate()
    end = time.time()

    with open(f"{LOG_PATH}/build.log", "w") as f:
        f.write(out + "\n" + err)

    metrics = {
        "exit_code": proc.returncode,
        "duration_sec": end - start,
    }
    with open(f"{LOG_PATH}/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)

if __name__ == "__main__":
    ensure_dirs()
    run_ant()
