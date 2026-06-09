from __future__ import annotations

import argparse
import json
import random
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, List


DEFAULT_CHUNK_SIZE = 100
DEFAULT_OVERLAP = 25
DEFAULT_DOCUMENTS_DIR = Path(__file__).resolve().parent / "documents"


@dataclass(frozen=True)
class DocumentChunk:
    file_name: str
    chunk_index: int
    start_token: int
    end_token: int
    text: str


def read_documents(documents_dir: Path) -> List[tuple[Path, str]]:
    documents: List[tuple[Path, str]] = []
    for file_path in sorted(documents_dir.glob("*.txt")):
        text = file_path.read_text(encoding="utf-8", errors="replace").strip()
        if text:
            documents.append((file_path, text))
    return documents


def tokenize(text: str) -> List[str]:
    return re.findall(r"\S+", text)


def chunk_tokens(tokens: List[str], chunk_size: int = DEFAULT_CHUNK_SIZE, overlap: int = DEFAULT_OVERLAP) -> List[List[str]]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap cannot be negative")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    if not tokens:
        return []

    step = chunk_size - overlap
    chunks: List[List[str]] = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))
        chunks.append(tokens[start:end])
        if end >= len(tokens):
            break
        start += step
    return chunks


def chunk_document(text: str, source_path: str, chunk_size: int = DEFAULT_CHUNK_SIZE, overlap: int = DEFAULT_OVERLAP) -> List[DocumentChunk]:
    tokens = tokenize(text)
    token_chunks = chunk_tokens(tokens, chunk_size=chunk_size, overlap=overlap)

    chunks: List[DocumentChunk] = []
    file_name = Path(source_path).name
    for chunk_index, token_chunk in enumerate(token_chunks):
        start_token = chunk_index * (chunk_size - overlap)
        end_token = start_token + len(token_chunk)
        chunks.append(
            DocumentChunk(
                file_name=file_name,
                chunk_index=chunk_index,
                start_token=start_token,
                end_token=end_token,
                text=" ".join(token_chunk),
            )
        )
    return chunks


def build_chunks_from_documents(
    documents_dir: Path = DEFAULT_DOCUMENTS_DIR,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> dict[str, List[DocumentChunk]]:
    all_chunks: dict[str, List[DocumentChunk]] = {}
    for file_path, text in read_documents(documents_dir):
        file_name = file_path.name
        all_chunks[file_name] = chunk_document(
            text=text,
            source_path=str(file_path),
            chunk_size=chunk_size,
            overlap=overlap,
        )
    return all_chunks


def ingest_documents(
    documents_dir: Path = DEFAULT_DOCUMENTS_DIR,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> dict[str, List[DocumentChunk]]:
    return build_chunks_from_documents(
        documents_dir=documents_dir,
        chunk_size=chunk_size,
        overlap=overlap,
    )


def get_random_chunks(
    chunks_by_document: dict[str, List[DocumentChunk]],
    count: int = 10,
    seed: int | None = None,
) -> List[DocumentChunk]:
    chunks = [chunk for chunk_list in chunks_by_document.values() for chunk in chunk_list]
    if not chunks:
        return []

    rng = random.Random(seed)
    sample_size = min(count, len(chunks))
    return rng.sample(chunks, sample_size)


def chunks_to_json(chunks: Iterable[DocumentChunk]) -> str:
    return json.dumps([asdict(chunk) for chunk in chunks], ensure_ascii=False, indent=2)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read documents and create token-based chunks for embedding.")
    parser.add_argument("--documents-dir", type=Path, default=DEFAULT_DOCUMENTS_DIR, help="Path to the documents directory.")
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE, help="Number of tokens per chunk.")
    parser.add_argument("--overlap", type=int, default=DEFAULT_OVERLAP, help="Number of overlapping tokens between chunks.")
    parser.add_argument("--json", action="store_true", help="Print chunks as JSON.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    chunks_by_document = ingest_documents(
        documents_dir=args.documents_dir,
        chunk_size=args.chunk_size,
        overlap=args.overlap,
    )
    chunks = [chunk for chunk_list in chunks_by_document.values() for chunk in chunk_list]

    if args.json:
        print(chunks_to_json(chunks))
        return

    print(f"Loaded {len(chunks)} chunks from {args.documents_dir}")
    for chunk in chunks[:5]:
        print(f"- {chunk.file_name}: {chunk.text[:80]}{'...' if len(chunk.text) > 80 else ''}")


if __name__ == "__main__":
    main()