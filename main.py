from fetcher import load_markdown_docs
from parser import normalize_doc
from chunker import chunk_doc
from indexer import persist

def main():
    raw = load_markdown_docs("sample_docs")
    norm = [normalize_doc(d) for d in raw]
    chunks = []
    for d in norm:
        chunks.extend(chunk_doc(d))
    persist(raw, norm, chunks)
    print("Done:", len(raw), "docs,", len(chunks), "chunks")

if __name__ == "__main__":
    main()
