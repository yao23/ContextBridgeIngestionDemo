import json
import os
from dataclasses import is_dataclass
from dataclasses import asdict
from models import IngestionState

def save(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def load_state():
    state = load_json("output/state.json", [])
    return {item["doc_id"]: item for item in state}

def load_existing_chunks():
    chunks = load_json("output/chunks.json", [])
    grouped = {}
    for chunk in chunks:
        grouped.setdefault(chunk["doc_id"], []).append(chunk)
    return grouped

def to_serializable(item):
    return asdict(item) if is_dataclass(item) else item

def persist(raw_docs, normalized_docs, chunks):
    save("output/raw.json", [to_serializable(d) for d in raw_docs])
    save("output/normalized.json", [to_serializable(d) for d in normalized_docs])
    save("output/chunks.json", [to_serializable(c) for c in chunks])

def persist_state(states):
    save("output/state.json", [asdict(s) for s in states])
