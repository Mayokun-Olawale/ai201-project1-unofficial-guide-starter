from __future__ import annotations

from typing import Dict, List

from config import N_RESULTS
from Embeddings import embed_and_store, get_collection, retrieve
from Ingestion import ingest_documents
from generation import generate_answer


def _flatten_documents(docs_by_file) -> List[dict]:
    chunks = []
    for file_name, chunk_list in docs_by_file.items():
        for chunk in chunk_list:
            chunks.append(
                {
                    "text": chunk.text,
                    "file_name": file_name,
                    "chunk_id": f"{file_name}::{chunk.chunk_index}",
                }
            )
    return chunks


def ensure_indexed() -> None:
    if get_collection().count() > 0:
        return

    docs_by_file = ingest_documents()
    chunks = _flatten_documents(docs_by_file)
    embed_and_store(chunks)


def ask(question: str) -> Dict[str, List[str] | str]:
    ensure_indexed()
    chunks = retrieve(question, n_results=N_RESULTS)
    answer = generate_answer(question, chunks)
    sources = list(dict.fromkeys(chunk["file_name"] for chunk in chunks if chunk.get("file_name")))
    return {"answer": answer, "sources": sources}