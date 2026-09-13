# EduMentor 🎓

## AI Teaching Assistant

EduMentor is an AI-powered teaching assistant designed to help students learn from their own study materials.

It allows students to upload PDFs, ask questions about their study material, generate quizzes, evaluate their performance, and analyze their learning progress.

---

## 🚀 Features

- 📚 PDF upload and processing
- 🔎 Semantic document search
- 🤖 AI-powered teaching assistant
- 🧠 Retrieval-Augmented Generation (RAG)
- 📝 AI-generated quizzes
- ✅ Automatic quiz evaluation
- 📊 Learning analytics
- 📈 Topic-wise performance analysis
- 🔐 User authentication
- 👤 Student dashboard
- ⚡ Real-time dashboard updates
- 📄 Source-aware answers from uploaded documents

---

## 🏗️ Architecture

```text
React Frontend
      │
      ▼
FastAPI Backend
      │
      ├──────────────► PostgreSQL
      │
      ├──────────────► FAISS
      │
      ├──────────────► Sentence Transformers
      │
      └──────────────► Hugging Face LLM



PDF
 │
 ▼
PyMuPDF
 │
 ▼
Text Extraction
 │
 ▼
Text Chunking
 │
 ▼
Sentence Transformers
 │
 ▼
Embeddings
 │
 ▼
FAISS
 │
 ▼
Relevant Chunks
 │
 ▼
Hugging Face LLM
 │
 ▼
AI Answer

🛠️ Technologies
Frontend
React
Vite
React Router
JavaScript
CSS
Backend
Python
FastAPI
SQLAlchemy
PostgreSQL
JWT Authentication
AI / ML
Hugging Face
Qwen
Sentence Transformers
FAISS
Retrieval-Augmented Generation
PDF Processing
PyMuPDF

Teaching_assistant/
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── utils/
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── README.md

