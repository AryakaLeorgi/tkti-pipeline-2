import os
import xml.etree.ElementTree as ET
import json

RAW_DIR = "data/raw/logchunks"
OUT_PARSED = "data/parsed/logchunks"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def find_all_xml(base):
    """Scan seluruh subfolder dan temukan file .xml"""
    for root, _, files in os.walk(base):
        for f in files:
            if f.endswith(".xml"):
                yield os.path.join(root, f)

def parse_failure_reasons(xml_path):
    """Parse file XML menjadi mapping log -> info"""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    mapping = {}
    for example in root.findall("Example"):
        logfile = example.find("Log").text.strip()
        chunk = example.find("Chunk").text.strip()
        keywords = [kw.strip() for kw in example.find("Keywords").text.split(",")]
        category = example.find("Category").text.strip()

        mapping[logfile] = {
            "failure_chunk": chunk,
            "keywords": keywords,
            "category": category
        }
    return mapping

def process_all():
    ensure_dir(OUT_PARSED)

    xml_folder = os.path.join(RAW_DIR, "build-failure-reason")

    # Scan seluruh XML
    xml_files = list(find_all_xml(xml_folder))
    print("Ditemukan XML:", len(xml_files))

    for xml_path in xml_files:
        print("Parsing XML:", xml_path)
        mapping = parse_failure_reasons(xml_path)

        for rel_log_path, info in mapping.items():
            log_path = os.path.join(RAW_DIR, "logs", rel_log_path)

            if not os.path.isfile(log_path):
                print("WARNING: log not found:", log_path)
                continue

            with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                log_text = f.read()

            out = {
                "log_path": rel_log_path,
                "failure_chunk": info["failure_chunk"],
                "keywords": info["keywords"],
                "category": info["category"],
                "full_log": log_text
            }

            out_path = os.path.join(OUT_PARSED, rel_log_path.replace("/", "__") + ".json")
            ensure_dir(os.path.dirname(out_path))
            with open(out_path, "w", encoding="utf-8") as fo:
                json.dump(out, fo, indent=2)

    print("Parsing selesai.")

if __name__ == "__main__":
    process_all()
