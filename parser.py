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

def extract_path_params(endpoint: str):
    return re.findall(r"\{([^}]+)\}", endpoint)

def extract_bullet_params(text: str):
    params = []
    for line in text.splitlines():
        match = re.match(r"^\s*-\s*`?([A-Za-z0-9_\-]+)`?\s*:", line.strip())
        if match:
            params.append(match.group(1))
    return params

def infer_auth_required(text: str, code_blocks: list[str]):
    searchable = "\n".join([text] + code_blocks).lower()
    auth_markers = ("bearer", "authorization", "api key", "requires auth", "requires authentication")
    return any(marker in searchable for marker in auth_markers)

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
            params = []
            if endpoint:
                params.extend(extract_path_params(endpoint))
            params.extend(extract_bullet_params(text))
            deduped_params = list(dict.fromkeys(params))
            sections.append(
                Section(
                    current_heading,
                    text,
                    code_blocks[:],
                    method,
                    endpoint,
                    deduped_params,
                    code_blocks[:],
                    infer_auth_required(text, code_blocks),
                )
            )
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
