from sentence_transformers import SentenceTransformer

_embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts: list[str]) -> list[list[float]]:
    embeddings = _embedding_model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()
