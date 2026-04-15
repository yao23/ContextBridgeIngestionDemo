from models import NormalizedDoc, Chunk

def infer_tags(text: str, method: str = "", endpoint: str = ""):
    keywords = ["auth","token","user","payment","post","get","bearer"]
    searchable = " ".join([text, method, endpoint]).lower()
    return [k for k in keywords if k in searchable]

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
            sec.method,
            sec.endpoint,
            sec.params,
            sec.examples,
            sec.auth_required,
            content.strip(),
            infer_tags(content, sec.method, sec.endpoint)
        ))
    return chunks
