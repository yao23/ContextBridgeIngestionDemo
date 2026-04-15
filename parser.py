import re
from models import RawDoc, NormalizedDoc, Section

def normalize_doc(raw_doc: RawDoc):
    lines = raw_doc.raw_text.splitlines()
    sections = []
    current_heading = "Introduction"
    buffer = []
    code_blocks = []
    in_code = False
    code_buffer = []

    def flush():
        nonlocal buffer, code_blocks
        text = "\n".join(buffer).strip()
        if text or code_blocks:
            sections.append(Section(current_heading, text, code_blocks[:]))
        buffer = []
        code_blocks = []

    for line in lines:
        if line.startswith("```"):
            in_code = not in_code
            if not in_code:
                code_blocks.append("\n".join(code_buffer))
                code_buffer = []
            continue

        if in_code:
            code_buffer.append(line)
            continue

        if re.match(r"^##+\s+", line):
            flush()
            current_heading = re.sub(r"^##+\s+", "", line).strip()
        else:
            buffer.append(line)

    flush()

    return NormalizedDoc(
        raw_doc.path.split("/")[-1].replace(".md", ""),
        raw_doc.path,
        raw_doc.title,
        sections
    )
