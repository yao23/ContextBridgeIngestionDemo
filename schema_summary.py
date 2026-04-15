import json


def main():
    with open("output/normalized.json", encoding="utf-8") as f:
        docs = json.load(f)

    for doc in docs:
        print(doc["title"])
        for section in doc["sections"]:
            summary = f"- {section['heading']}"
            if section.get("method") and section.get("endpoint"):
                summary += f": {section['method']} {section['endpoint']}"
            print(summary)
            if section.get("params"):
                print(f"  params: {', '.join(section['params'])}")
            if section.get("auth_required"):
                print("  auth: required")
            if section.get("examples"):
                print(f"  examples: {len(section['examples'])}")
        print()


if __name__ == "__main__":
    main()
