import json
import sys


EXPECTED = {
    "auth": {
        "heading": "Create Token",
        "method": "POST",
        "endpoint": "/v1/token",
        "params": ["client_id", "client_secret"],
        "response_fields": ["access_token", "expires_in"],
        "status_codes": ["200", "401"],
        "auth_required": True,
    },
    "users": {
        "heading": "Get User",
        "method": "GET",
        "endpoint": "/v1/users/{id}",
        "params": ["id", "expand"],
        "response_fields": ["id", "email", "profile"],
        "status_codes": ["200", "404"],
        "auth_required": True,
    },
}


def load_sections():
    with open("output/normalized.json", encoding="utf-8") as f:
        docs = json.load(f)
    return {doc["doc_id"]: doc["sections"][0] for doc in docs}


def assert_equal(label, actual, expected):
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected}, got {actual}")


def main():
    sections = load_sections()

    for doc_id, expected in EXPECTED.items():
        if doc_id not in sections:
            raise AssertionError(f"missing doc: {doc_id}")
        section = sections[doc_id]
        assert_equal(f"{doc_id}.heading", section["heading"], expected["heading"])
        assert_equal(f"{doc_id}.method", section["method"], expected["method"])
        assert_equal(f"{doc_id}.endpoint", section["endpoint"], expected["endpoint"])
        assert_equal(f"{doc_id}.params", section["params"], expected["params"])
        assert_equal(
            f"{doc_id}.response_fields",
            section["response_fields"],
            expected["response_fields"],
        )
        assert_equal(
            f"{doc_id}.status_codes",
            section["status_codes"],
            expected["status_codes"],
        )
        assert_equal(
            f"{doc_id}.auth_required",
            section["auth_required"],
            expected["auth_required"],
        )

    print("Extraction evaluation passed for sample_docs.")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as exc:
        print(f"Extraction evaluation failed: {exc}")
        sys.exit(1)
