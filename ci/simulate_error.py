import random
import json
import os

LOG_PATH = "ci/error_log.json"
os.makedirs("ci", exist_ok=True)

failure_types = [
    "MissingDependency",
    "NetworkTimeout",
    "PackageVersionConflict",
    "TestAssertionError",
    "ContainerBuildFailure",
    "KubernetesConfigInvalid",
    "SecurityVulnerabilityFound"
]

# Random trigger failure
trigger_failure = random.random() < 0.35  # 35% chance

if trigger_failure:
    failure = random.choice(failure_types)
    message = f"Simulated CI failure: {failure}"
else:
    failure = "None"
    message = "No CI failure simulated."

data = {
    "ci_failure": failure,
    "message": message
}

with open(LOG_PATH, "w") as f:
    json.dump(data, f, indent=4)

print(f"Simulated failure: {failure}")
