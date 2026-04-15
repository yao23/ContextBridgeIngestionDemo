import re
from models import RawDoc, NormalizedDoc, Section

HTTP_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")

def extract_endpoint_signature(text: str):
    for line in text.splitlines():
        stripped = line.strip()
        match = re.match(rf"^({'|'.join(HTTP_METHODS)})\s+(\S+)", stripped)
        if match:
            return match.group(1), match.group(2)
    return "", ""

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
        text_lines = [line for line in buffer if line.strip()]
        text = "\n".join(text_lines).strip()
        if text or code_blocks:
            method, endpoint = extract_endpoint_signature(text)
            sections.append(Section(current_heading, text, code_blocks[:], method, endpoint))
        buffer = []
        code_blocks = []

    for line in lines:
        if not sections and not buffer and line.strip() == f"# {raw_doc.title}":
            continue

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
        elif line.startswith("# "):
            continue
        else:
            buffer.append(line)

    flush()

    return NormalizedDoc(
        raw_doc.path.split("/")[-1].replace(".md", ""),
        raw_doc.path,
        raw_doc.title,
        sections
    )
