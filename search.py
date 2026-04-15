import json
import re
import sys
from collections import Counter

def tokenize(text):
    return re.findall(r"[a-z0-9_]+", text.lower())

def score(q, record):
    query_terms = tokenize(q)
    searchable_text = " ".join(
        [
            record["title"],
            record["section"],
            record.get("method", ""),
            record.get("endpoint", ""),
            " ".join(record.get("params", [])),
            record["content"],
            " ".join(record["tags"]),
        ]
    )
    content_terms = tokenize(searchable_text)
    counts = Counter(content_terms)
    return sum(counts[term] for term in query_terms)

def main():
    if len(sys.argv) < 2:
        print("Usage: python search.py 'query'")
        return

    q = sys.argv[1]
    with open("output/chunks.json", encoding="utf-8") as f:
        data = json.load(f)

    ranked = []
    for item in data:
        item_score = score(q, item)
        if item_score > 0:
            ranked.append({**item, "score": item_score})

    ranked.sort(key=lambda x: x["score"], reverse=True)

    for r in ranked[:5]:
        print(f"[score={r['score']}] {r['title']} > {r['section']}")
        if r.get("method") and r.get("endpoint"):
            print(f"endpoint={r['method']} {r['endpoint']}")
        if r.get("params"):
            print(f"params={', '.join(r['params'])}")
        if r.get("auth_required"):
            print("auth=required")
        print(f"tags={', '.join(r['tags']) if r['tags'] else 'none'}")
        print(r["content"][:200])
        print("---")

    if not ranked:
        print("No matching chunks found.")

if __name__ == "__main__":
    main()
