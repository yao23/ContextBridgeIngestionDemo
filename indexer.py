import json, os
from dataclasses import asdict

def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def persist(raw_docs, normalized_docs, chunks):
    save("output/raw.json", [asdict(d) for d in raw_docs])
    save("output/normalized.json", [asdict(d) for d in normalized_docs])
    save("output/chunks.json", [asdict(c) for c in chunks])
