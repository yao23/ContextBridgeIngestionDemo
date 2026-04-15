#!/usr/bin/env bash

set -euo pipefail

echo "==> Running ingestion pipeline"
python3 main.py
echo

echo "==> Showing extracted API schema"
python3 schema_summary.py
echo

echo "==> Running sample search: create token"
python3 search.py "create token"
echo

echo "==> Running sample search: user profile 404"
python3 search.py "user profile 404"
