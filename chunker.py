from models import NormalizedDoc, Chunk

def infer_tags(text: str):
    keywords = ["auth","token","user","payment","post","get"]
    return [k for k in keywords if k in text.lower()]

def chunk_doc(doc: NormalizedDoc):
    chunks = []
    for i, sec in enumerate(doc.sections):
        content = sec.text + "\n\n" + "\n".join(sec.code_blocks)
        chunks.append(Chunk(
            f"{doc.doc_id}:{i}",
            doc.doc_id,
            doc.path,
            doc.title,
            sec.heading,
            content.strip(),
            infer_tags(content)
        ))
    return chunks
