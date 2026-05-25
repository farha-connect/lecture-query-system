# Lecture Query System

I built this because I kept scrubbing through 2-hour lecture recordings trying to find one concept I half-remembered. This tool lets you upload any lecture, ask it questions in plain English, and get answers with the exact timestamp to jump to.

Runs entirely on your machine. Nothing leaves your device.

Presented at **ICIDSSD 2026**, 6th International Conference on ICT for Digital, Smart, and Sustainable Development.

---

## What it does

- Upload any audio or video lecture (MP4, MP3, WAV, M4A)
- Transcribes it automatically using OpenAI Whisper
- Stores transcript chunks in a ChromaDB vector database
- Answers your questions with exact timestamps pointing back to the source
- No internet required fully local, no data sent anywhere

---

## Tech stack

| Component | Technology |
|---|---|
| Transcription | OpenAI Whisper |
| Semantic Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector Database | ChromaDB |
| LLM | Llama 3.2 via Ollama |
| Frontend | Streamlit |

---

## How to run

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/lecture-query-system
cd lecture-query-system
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Install and start Ollama**

Download from https://ollama.com, then:
```bash
ollama serve
```

**4. Create the custom model**
```bash
ollama create mylecture -f Modelfile
```

**5. Run the app**
```bash
streamlit run app.py
```

**6. Login**

Username: admin
Password: admin123

---

## How it works

1. You upload a recording via the Streamlit interface
2. Whisper transcribes it into timestamped segments
3. Segments are chunked and embedded using SentenceTransformers
4. Embeddings are stored in ChromaDB
5. When you ask a question, it gets embedded and matched against the stored chunks
6. Top 3 matching chunks go to Llama 3.2 via Ollama
7. The LLM returns an answer with the source timestamp

---

## Requirements

- Python 3.10+
- 8GB RAM minimum (16GB recommended for smoother performance)
- 10GB free storage for model weights
- Ollama installed locally

Tested on an 8-minute lecture recording. Works best with clear audio. Still being improved — feel free to open an issue if something breaks.
