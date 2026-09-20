# Vector Database
import chromadb
from chromadb.config import Settings
from .embedding import embed_texts
_chroma_client = chromadb.Client(
    Settings(anonymized_telemetry=False)
    )

def get_or_create_collection(session_id: str):
    return _chroma_client.get_or_create_collection(name=session_id)

def index_chunks(session_id: str, chunks: list[dict]) -> int:
    collection = get_or_create_collection(session_id)
    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(texts)
    ids = [f"chunk-{c['id']}" for c in chunks]

    collection.add(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=[{"chunk_id": c["id"]} for c in chunks],
    )
    return len(chunks)