import argparse
import json
from ant_parser.parser import AntParser
from ml.infer import infer

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--issue", required=False, default="Build failed due to unknown error")
    args = parser.parse_args()

    # Parse Ant build.xml
    ant = AntParser(args.input)
    g, feats = ant.parse()

    # Run ML inference
    result = infer(g, feats, args.issue)

    # Convert result to a JSON-safe format
    output = {
        "prediction": int(result)  # ensure numpy.int64 → int
    }

    # Write JSON output
    with open(args.output, "w") as f:
        f.write(json.dumps(output, indent=2))

if __name__ == "__main__":
    run()
