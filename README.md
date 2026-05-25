# Lecture Query System

A fully local, privacy-first AI assistant that lets you ask 
natural language questions about any recorded lecture or session 
and receive timestamped, sourced answers.

Presented at ICIDSSD 2026, 6th International Conference on ICT 
for Digital, Smart, and Sustainable Development.

---

## What It Does

- Upload any audio or video lecture (MP4, MP3, WAV, M4A)
- Automatically transcribes it using OpenAI Whisper
- Stores transcript chunks in a ChromaDB vector database
- Answers your natural language questions with exact video timestamps
- Runs entirely on your local machine — no internet, no data sent anywhere

---

## Tech Stack

| Component | Technology |
|---|---|
| Transcription | OpenAI Whisper |
| Semantic Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector Database | ChromaDB |
| LLM | Llama 3.2 via Ollama |
| Frontend | Streamlit |

---

## How to Run

### 1. Clone the repository
git clone https://github.com/yourusername/lecture-query-system
cd lecture-query-system

### 2. Install dependencies
pip install -r requirements.txt

### 3. Install and start Ollama
Download from https://ollama.com
Then run: ollama serve

### 4. Create the custom model
ollama create mylecture -f Modelfile

### 5. Run the app
streamlit run app.py

### 6. Login
Username: admin
Password: admin123

---

## System Architecture

The pipeline works as follows:
1. User uploads a recording via the Streamlit interface
2. Whisper transcribes the audio into timestamped segments
3. Segments are chunked and embedded using SentenceTransformers
4. Embeddings are stored in ChromaDB
5. User queries are embedded and matched against ChromaDB
6. Top 3 matching chunks are passed to Llama 3.2 via Ollama
7. LLM generates a detailed answer with source timestamp

---

## Requirements

- Python 3.10+
- 8GB RAM minimum (16GB recommended)
- 10GB free storage (for model weights)
- Ollama installed locally
