"""
Retrieval
Alurnya gini:
1. Pertanyaan --> vector (Embedding)
2. ChromaDB hitung jarak vector pertanyaan ke SEMUA chunk tersimpan
3. Ambil top_k chunk dengan jarak terdekat (paling mirip maknanya)
"""
from .embedding import embed_texts
from .vector_database import get_or_create_collection

def retrieve_relevant_chunks(session_id: str, question: str, top_k: int = 3) -> list[dict]:
    collection = get_or_create_collection(session_id)
    query_embedding = embed_texts([question])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    retrieved = []
    for doc, distance, metadata in zip(
        results["documents"][0], results["distances"][0], results["metadatas"][0]
    ):
        retrieved.append({
            "text": doc,
            "chunk_id": metadata["chunk_id"],
            "similarity_score": 1 - distance,
        })
    return retrieved
