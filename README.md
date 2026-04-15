# ContextBridge Ingestion Demo

This project is a lightweight data-ingestion demo for API documentation. It reads local markdown docs, normalizes them into structured sections, chunks them in a heading-aware way, and writes JSON artifacts that are easy to inspect or search.

## What it shows

- Structure-aware ingestion instead of raw text scraping
- Metadata attached to chunks for downstream coding-agent retrieval
- Incremental ingestion using content hashes
- Lightweight endpoint extraction for API sections
- Parameter, example, and auth-hint extraction
- Response-field and status-code extraction
- A simple keyword search CLI over the generated chunks

## Project layout

- `main.py`: runs the ingestion pipeline
- `fetcher.py`: loads markdown docs and computes content hashes
- `parser.py`: normalizes markdown into sections and code blocks
- `chunker.py`: emits chunk records with basic tags
- `indexer.py`: persists outputs and ingestion state
- `search.py`: searches chunked output by keyword overlap
- `schema_summary.py`: prints a compact API-schema view from normalized docs
- `demo.sh`: runs the end-to-end interview demo flow
- `sample_docs/`: example API docs to ingest
- `output/`: generated artifacts

## Run it

```bash
python3 main.py
python3 search.py "create token"
python3 schema_summary.py
bash demo.sh
```

## Output files

- `output/raw.json`: raw fetched markdown docs
- `output/normalized.json`: normalized document structure
- `output/chunks.json`: searchable chunk records
- `output/state.json`: ingestion state used for incremental runs
- Endpoint and HTTP method metadata are included when the parser can detect them
- Path params, bullet-listed params, examples, and auth hints are extracted when present
- Response fields and status codes are extracted from simple markdown patterns

## Incremental behavior

Each markdown file gets a SHA-256 content hash. On re-run, unchanged docs reuse their existing chunks, while changed docs are re-normalized and re-chunked.

## Good interview talking points

- Preserving section boundaries and examples improves retrieval quality for coding agents.
- Stable document identities and content hashes let the pipeline avoid full rebuilds.
- The next natural extension is nested JSON-schema extraction and richer validation rules.

## Suggested demo flow

1. Start with `bash demo.sh` to show the whole ingestion-to-retrieval path quickly.
2. Call out that the pipeline preserves semantic structure instead of flattening docs into raw text.
3. Point at `schema_summary.py` output to show extracted method, endpoint, params, auth, response fields, and status codes.
4. Use `search.py "create token"` or `search.py "user profile 404"` to show that retrieval benefits from structured metadata, not just keyword matches.
5. Close by explaining that incremental ingestion plus pipeline versioning prevents unnecessary rebuilds while still invalidating stale derived artifacts after parser changes.

## Short interview script

You can use this framing almost verbatim:

“I modeled this as a lightweight ingestion pipeline for coding-agent-friendly API docs. The main design goal is preserving structure during normalization and chunking, because retrieval quality depends on keeping endpoints, examples, auth hints, params, and response details together.”

“The pipeline reads markdown docs, normalizes them into sections, extracts API metadata like method, endpoint, params, response fields, and status codes, and then writes searchable chunk artifacts. I also added incremental ingestion with content hashes and pipeline versioning so unchanged docs can be reused safely, while parser changes still invalidate stale derived output.”

“For the retrieval side, I’m showing a simple keyword scorer, but the important point is the shape of the indexed data. The next natural step would be embedding-based ranking or richer schema extraction, but even this small demo already shows how ingestion quality drives downstream agent usefulness.”
