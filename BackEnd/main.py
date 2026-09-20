import os
import tempfile
import uuid

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rag_pipeline.text_extraction import extract_text
from rag_pipeline.chunking import smart_chunk_text
from rag_pipeline.vector_database import index_chunks
from rag_pipeline.retrieval import retrieve_relevant_chunks
from rag_pipeline.llm_api import ask_llm

app = FastAPI(title="AI Study Assistant - RAG Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
sessions: dict[str, dict] = {}
class AskRequest(BaseModel):
    session_id: str
    question: str

@app.post("/upload")
async def upload_material(file: UploadFile = File(...)):
    """
    Tahap: Text Extraction -> Chunking -> Embedding -> Vector Database
    """
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # Text Extraction
        raw_text = extract_text(tmp_path, file.filename)
        if not raw_text.strip():
            raise HTTPException(400, "Tidak ada teks yang bisa diekstrak dari file ini.")

        # Chunking
        chunks = smart_chunk_text(raw_text)

        # Embedding + Vector Database
        session_id = str(uuid.uuid4())
        indexed_count = index_chunks(session_id, chunks)

        sessions[session_id] = {"filename": file.filename, "chunk_count": indexed_count}

        return {
            "session_id": session_id,
            "filename": file.filename,
            "chunk_count": indexed_count,
        }
    finally:
        os.remove(tmp_path)


@app.post("/ask")
async def ask_question(req: AskRequest):
    """
    Tahap: Retrieval -> LLM API
    """
    if req.session_id not in sessions:
        raise HTTPException(404, "Sesi tidak ditemukan. Upload materi dulu.")

    # Retrieval
    retrieved = retrieve_relevant_chunks(req.session_id, req.question, top_k=3)

    # LLM API
    answer_text = ask_llm(req.question, retrieved)

    return {
        "answer": answer_text,
        "sources": [
            {"chunk_id": r["chunk_id"], "text": r["text"], "score": r["similarity_score"]}
            for r in retrieved
        ],
    }

# Debug BackEnd 
@app.get("/health")
async def health_check():
    return {"status": "ok"}
