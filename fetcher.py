from pathlib import Path
import hashlib
from models import RawDoc

def load_markdown_docs(input_dir: str):
    docs = []
    for path in Path(input_dir).glob("*.md"):
        raw_text = path.read_text(encoding="utf-8")
        title = raw_text.splitlines()[0].lstrip("# ").strip() if raw_text else path.stem
        content_hash = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
        docs.append(RawDoc(str(path), title, raw_text, content_hash))
    return docs
