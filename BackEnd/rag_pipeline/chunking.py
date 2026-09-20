import re

def smart_chunk_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 150,
    ) -> list[dict]:
    clean_text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r"(?<=[.!?])\s+", clean_text)

    chunks = []
    current_chunk = ""
    chunk_id = 0

    for sentence in sentences:
        if len(current_chunk) + len(sentence) > chunk_size and current_chunk:
            chunks.append({"id": chunk_id, "text": current_chunk.strip()})
            chunk_id += 1
            # 800(150 cHuNk)
            current_chunk = current_chunk[-overlap:] + " " + sentence
        else:
            current_chunk += " " + sentence

    if current_chunk.strip():
        chunks.append({"id": chunk_id, "text": current_chunk.strip()})

    return chunks