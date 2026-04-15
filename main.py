from fetcher import load_markdown_docs
from parser import normalize_doc
from chunker import chunk_doc
from indexer import load_existing_chunks, load_state, persist, persist_state
from models import IngestionState

def main():
    raw = load_markdown_docs("sample_docs")
    previous_state = load_state()
    previous_chunks = load_existing_chunks()
    norm = []
    chunks = []
    states = []
    changed = 0

    for raw_doc in raw:
        states.append(
            IngestionState(
                doc_id=raw_doc.path.split("/")[-1].replace(".md", ""),
                path=raw_doc.path,
                title=raw_doc.title,
                content_hash=raw_doc.content_hash,
            )
        )

        previous = previous_state.get(states[-1].doc_id)
        if previous and previous["content_hash"] == raw_doc.content_hash:
            chunks.extend(previous_chunks.get(states[-1].doc_id, []))
            continue

        normalized = normalize_doc(raw_doc)
        norm.append(normalized)
        chunks.extend(chunk_doc(normalized))
        changed += 1

    if len(norm) < len(raw):
        for raw_doc in raw:
            doc_id = raw_doc.path.split("/")[-1].replace(".md", "")
            if any(doc.doc_id == doc_id for doc in norm):
                continue
            previous = previous_state.get(doc_id)
            if previous:
                norm.append(normalize_doc(raw_doc))

    persist(raw, norm, chunks)
    persist_state(states)
    print("Done:", len(raw), "docs,", len(chunks), "chunks,", changed, "changed")

if __name__ == "__main__":
    main()
