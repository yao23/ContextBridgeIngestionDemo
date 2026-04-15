import json, sys

def score(q, c):
    return sum(c.lower().count(w) for w in q.lower().split())

def main():
    q = sys.argv[1]
    data = json.load(open("output/chunks.json"))
    ranked = sorted(data, key=lambda x: score(q, x["content"]), reverse=True)[:3]
    for r in ranked:
        print(r["title"], ">", r["section"])
        print(r["content"][:200])
        print("---")

if __name__ == "__main__":
    main()
