# LLM API
import os
from google import genai

_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def build_context_text(retrieved_chunks: list[dict]) -> str:
    if not retrieved_chunks:
        return "(Tidak ditemukan potongan materi yang relevan.)"

    return "\n\n".join(
        f"[Sumber {i + 1}, skor kemiripan {c['similarity_score']:.2f}]\n{c['text']}"
        for i, c in enumerate(retrieved_chunks)
    )

def ask_llm(question: str, retrieved_chunks: list[dict]) -> str:
    context_text = build_context_text(retrieved_chunks)

    prompt = f"""
Kamu adalah asisten belajar berbasis RAG.

Jawab HANYA berdasarkan potongan materi yang diberikan.
Jika informasi tidak cukup atau tidak ditemukan di materi,
katakan dengan jujur bahwa informasi tidak ditemukan di materi.

Potongan materi relevan:
{context_text}

Pertanyaan user:
{question}
"""

    interaction = _client.interactions.create(
        model="gemini-3.6-flash",
        input=prompt,
    )

    return interaction.output_text