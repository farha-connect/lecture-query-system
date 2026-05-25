import os
import chromadb
from chromadb.utils import embedding_functions
import streamlit as st

DB_DIR = "data/vectordb"

@st.cache_resource
def get_embedder():
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

@st.cache_resource
def get_chroma_client():
    return chromadb.PersistentClient(path=DB_DIR)

def get_collection():
    client = get_chroma_client()
    embedder = get_embedder()
    return client.get_or_create_collection(
        name="lectures",
        embedding_function=embedder
    )

def save_transcript(transcript, video_name):
    collection = get_collection()
    segments = transcript["segments"]
    chunks_saved = 0
    for i in range(0, len(segments), 5):
        chunk_segments = segments[i:i+5]
        text_chunk = " ".join([s["text"] for s in chunk_segments]).strip()
        start_time = chunk_segments[0]["start"]
        doc_id = f"{video_name}_chunk_{i}"
        start_str = f"{int(start_time // 60):02d}:{int(start_time % 60):02d}"
        collection.add(
            documents=[text_chunk],
            metadatas=[{"video_name": video_name, "timestamp": start_str, "start_seconds": start_time}],
            ids=[doc_id]
        )
        chunks_saved += 1
    return chunks_saved

def list_videos():
    collection = get_collection()
    data = collection.get(include=["metadatas"])
    videos = set()
    for meta in data["metadatas"]:
        if meta and "video_name" in meta:
            videos.add(meta["video_name"])
    return list(videos)

def delete_video(video_name):
    collection = get_collection()
    collection.delete(where={"video_name": video_name})

def search(query, video_name, n_results=3):
    collection = get_collection()
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where={"video_name": video_name}
    )
    return results