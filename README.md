# Lecture Query System

I built this because I kept scrubbing through 2-hour lecture recordings trying to find one concept I half-remembered. This tool lets you upload any lecture, ask it questions in plain English, and get answers with the exact timestamp to jump to.

Runs entirely on your machine. Nothing leaves your device.

Presented at ICIDSSD 2026, 6th International Conference on ICT for Digital, Smart, and Sustainable Development.

---

## What it does

- Upload any audio or video lecture (MP4, MP3, WAV, M4A)
- Transcribes it automatically using OpenAI Whisper
- Stores transcript chunks in a ChromaDB vector database
- Answers your questions with exact timestamps pointing back to the source
- No internet required fully local, no data sent anywhere

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Transcription | OpenAI Whisper |
| Semantic Embeddings | SentenceTransformers (all-MiniLM-L6-v2) |
| Vector Database | ChromaDB |
| LLM | Llama 3.2 via Ollama |
| Frontend | Streamlit |

---

## How to Run

**1. Clone the repo**
```bash
git clone https://github.com/farha-connect/lecture-query-system
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

Username: `admin` Password: `admin123`

---

## How it Works

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

---

## Privacy-First Design Rationale

A core design constraint was keeping everything local. Lecture recordings often contain sensitive academic content, and uploading them to cloud APIs creates a privacy risk for students and institutions. Every component, transcription, embedding, retrieval, and inference  runs on the user's machine. No data leaves the device, no API keys needed, works fully offline.

This makes the system viable in institutional settings where cloud-based tools are restricted or unavailable, and for students who are simply uncomfortable with their course material being processed by third-party servers.

---

## Design Decisions & Tradeoffs

**Why semantic chunking over sentence-level splitting?**
Sentence-level splits frequently break mid-explanation. Overlapping semantic chunks preserve the explanatory arc of a lecture segment, so the retrieved context actually contains a complete thought rather than a fragment.

**Why SentenceTransformers for embeddings?**
all-MiniLM-L6-v2 is fast, lightweight, and runs locally without GPU requirements — important since the whole point is avoiding cloud dependency. The tradeoff is slightly lower semantic precision than larger embedding models, but adequate for lecture retrieval at this scale.

**Why a custom Modelfile with Llama 3.2?**
The custom Modelfile lets the prompt be tuned specifically for timestamp-grounded answering — instructing the model to cite sources rather than generate freely. Without this, the LLM tends to answer from general knowledge rather than the retrieved lecture content.

---

## Limitations & Future Work

- Validated on short recordings (8 minutes). Performance on full 2-hour lectures, especially with varying audio quality, hasn't been formally evaluated yet
- No user study has conducted  a rigorous comparison of time-to-answer versus manual scrubbing across multiple participants is the most important next step
- Whisper degrades on low-quality audio or heavy accents
- Single-turn queries only,  multi-turn conversational retrieval would be a natural extension
- No speaker diarisation:  can't distinguish instructor from student in Q&A sections

Tested on an 8-minute lecture recording. Works best with clear audio. Still being improved — feel free to open an issue if something breaks.
