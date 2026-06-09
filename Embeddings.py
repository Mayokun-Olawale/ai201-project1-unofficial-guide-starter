from __future__ import annotations

from typing import Iterable, List

import chromadb
from chromadb.utils import embedding_functions

from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS

# Embedding function and ChromaDB client are initialized once at module load.
# sentence-transformers downloads the model on first use — this may take
# 30–60 seconds the very first time. Subsequent runs use a local cache.
_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=_ef,
    metadata={"hnsw:space": "cosine"},
)


def get_collection():
    """Return the ChromaDB collection. Used by app.py during ingestion."""
    return _collection


def _normalize_chunk(chunk):
    """Convert a chunk object or dict into the flat shape used by Chroma."""
    if isinstance(chunk, dict):
        text = chunk["text"]
        file_name = chunk.get("file_name")
        chunk_id = chunk.get("chunk_id")
    else:
        text = chunk.text
        file_name = getattr(chunk, "file_name", None)
        chunk_index = getattr(chunk, "chunk_index", None)
        start_token = getattr(chunk, "start_token", None)
        end_token = getattr(chunk, "end_token", None)
        chunk_id = getattr(chunk, "chunk_id", None)
        if chunk_id is None:
            if file_name is not None and chunk_index is not None:
                chunk_id = f"{file_name}_{chunk_index}"
            else:
                chunk_id = f"chunk_{start_token}_{end_token}"
    return {
        "text": text,
        "file_name": file_name,
        "chunk_id": chunk_id,
    }


def embed_and_store(chunks):
    """
    Embed a list of chunks and store them in the vector database.

    This follows the provided guardrail shape, but uses `file_name` for this
    project because these documents are articles, not games.

    `_collection.add()` takes three parallel lists:
      - documents: raw text strings
      - metadatas: one dict per chunk, storing the source file name
      - ids: unique chunk identifiers
    """
    normalized = [_normalize_chunk(chunk) for chunk in chunks]

    _collection.add(
        documents=[chunk["text"] for chunk in normalized],
        metadatas=[{"file_name": chunk["file_name"]} for chunk in normalized],
        ids=[chunk["chunk_id"] for chunk in normalized],
    )
    print(f"Stored {_collection.count()} total chunks in the vector database.")


def retrieve(query, n_results=N_RESULTS):
    if _collection.count() == 0:
        return []

    results = _collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    return [
        {
            "text": document,
            "file_name": metadata.get("file_name"),
            "distance": distance,
        }
        for document, metadata, distance in zip(documents, metadatas, distances)
    ]
