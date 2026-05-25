import requests
import json
from vectorstore import search

def ask_ollama_stream(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mylecture",
                "prompt": prompt,
                "stream": True
            },
            stream=True
        )
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                yield data["response"]
    except requests.exceptions.ConnectionError:
        yield "Error: Could not connect to local Ollama instance. Is Ollama running?"

def ask(question, video_name):
    results = search(question, video_name, n_results=3)
    
    if not results['documents'] or len(results['documents'][0]) == 0:
        def empty_stream():
            yield "I couldn't find any relevant information in this video."
        return empty_stream(), []
    
    context_chunks = results['documents'][0]
    metadata_chunks = results['metadatas'][0]
    context_text = "\n\n---\n\n".join(context_chunks)
    
    prompt = f"""
    You are a 'Detailed Academic Researcher'. Your task is to answer questions based strictly on the provided lecture context. 
    You MUST provide an EXHAUSTIVE, highly detailed, multi-paragraph explanation of at least 350 words.
    You must include exact quotes where relevant.
    End with a 'Key Takeaways' NUMBERED list. Format: '1. ', '2. ' with double newline between each point.
    Do NOT use citations, brackets, or academic markers. Weave quotes naturally.
    Use ONLY the context below. If unsure, say "I don't know based on the lecture."
    
    Context:
    {context_text}
    
    Question: {question}
    Answer:
    """
    
    sources = []
    for meta, chunk in zip(metadata_chunks, context_chunks):
        sources.append({"timestamp": meta["timestamp"], "text": chunk})
        
    return ask_ollama_stream(prompt), sources