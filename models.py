from dataclasses import dataclass, field
from typing import List

@dataclass
class RawDoc:
    path: str
    title: str
    raw_text: str
    content_hash: str

@dataclass
class Section:
    heading: str
    text: str
    code_blocks: List[str] = field(default_factory=list)
    method: str = ""
    endpoint: str = ""

@dataclass
class NormalizedDoc:
    doc_id: str
    path: str
    title: str
    sections: List[Section]

@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    path: str
    title: str
    section: str
    method: str
    endpoint: str
    content: str
    tags: List[str]

@dataclass
class IngestionState:
    doc_id: str
    path: str
    title: str
    content_hash: str
    pipeline_version: str
