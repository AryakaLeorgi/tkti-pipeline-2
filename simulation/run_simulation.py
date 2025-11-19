import pandas as pd
import random
import sys

output = sys.argv[sys.argv.index("--output") + 1]

df = pd.DataFrame({
    "build_time": [random.randint(50, 150)],
    "tests_failed": [random.randint(0, 5)],
    "commit_size": [random.randint(5, 500)],
})

df.to_csv(output, index=False)
print("Saved:", output)
