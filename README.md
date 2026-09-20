# AI Study Assistant - RAG

AI Study Assistant adalah aplikasi untuk membantu memahami materi pembelajaran dari file yang diunggah. Aplikasi menggunakan pendekatan Retrieval-Augmented Generation (RAG), sehingga jawaban dibuat berdasarkan isi dokumen yang diberikan.

## Teknologi

### Frontend
- React
- JavaScript
- Vite

### Backend
- Python
- FastAPI

### RAG
- Sentence Transformers
- ChromaDB
- Gemini API

## Struktur Project

```text
Study-Asistant---RAG/
├── BackEnd/
│   ├── main.py
│   ├── requirements.txt
│   └── rag_pipeline/
│       ├── text_extraction.py
│       ├── chunking.py
│       ├── embedding.py
│       ├── vector_database.py
│       ├── retrieval.py
│       └── llm_api.py
│
├── FrontEnd/
│   ├── App.jsx
│   ├── App.css
│   ├── main.jsx
│   ├── index.html
│   ├── package.json
│   └── package-lock.json
│
└── README.md