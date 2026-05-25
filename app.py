import streamlit as st
import os
import json
from transcriber import transcribe
from vectorstore import save_transcript, list_videos, delete_video
from rag import ask

st.set_page_config(page_title="Lecture Query System", page_icon="🎓", layout="wide")

if "theme" not in st.session_state:
    st.session_state["theme"] = "Light"

if st.session_state["theme"] == "Dark":
    theme_css = """
    <style>
    /* Pure Black and White Dark Mode */
    .stApp, .main, header { background-color: #000000 !important; color: #ffffff !important; }
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div { background-color: #000000 !important; border-right: 1px solid #ffffff !important; }
    svg { fill: #ffffff !important; color: #ffffff !important; }
    .stTextInput div[data-baseweb="input"], .stTextInput div[data-baseweb="base-input"] { background-color: #000000 !important; border: 1px solid #ffffff !important; }
    .stTextInput input { background-color: #000000 !important; color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; }
    [data-testid="stFileUploader"] { background-color: transparent !important; border: none !important; }
    [data-testid="stFileUploaderDropzone"], [data-testid="stFileUploadDropzone"], .stFileUploader section { background-color: #000000 !important; color: #ffffff !important; border: 1px solid #ffffff !important; border-radius: 8px !important; padding: 20px !important; }
    [data-testid="stFileUploader"] *, [data-testid="stFileUploaderDropzone"] *, [data-testid="stFileUploadDropzone"] *, .stFileUploader * { color: #ffffff !important; }
    .recording-pill { background-color: #000000 !important; color: #ffffff !important; border: 1px solid #ffffff !important; }
    .timestamp-badge { background-color: #ffffff !important; color: #000000 !important; border: 1px solid #ffffff !important; }
    .source-title { background-color: #ffffff !important; color: #000000 !important; }
    p, h1, h2, h3, h4, h5, h6, span, label { color: #ffffff !important; }
    button, [data-testid="baseButton-secondary"], [data-testid="baseButton-primary"] { background-color: #000000 !important; color: #ffffff !important; border: 1px solid #ffffff !important; }
    button *, [data-testid="baseButton-secondary"] *, [data-testid="baseButton-primary"] * { color: #ffffff !important; background-color: transparent !important; }
    header button, header [role="button"] { background-color: transparent !important; border: none !important; }
    header * { color: #ffffff !important; }
    </style>
    """
else:
    theme_css = """
    <style>
    .stApp, .main { background-color: #ffffff !important; color: #000000 !important; }
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div { background-color: #f8f9fa !important; border-right: 1px solid #ddd !important; }
    .recording-pill { background-color: #f0f0f0 !important; color: #333 !important; }
    .timestamp-badge { background-color: #f8f9fa !important; color: #333 !important; border: 1px solid #ddd !important; }
    .source-title { background-color: black !important; color: white !important; }
    </style>
    """

st.markdown(theme_css, unsafe_allow_html=True)

# Common CSS
st.markdown("""
<style>
.stChatMessage { border-radius: 10px; padding: 10px; }
.recording-pill { border-radius: 5px; padding: 5px 10px; margin: 5px 0; font-weight: bold; font-family: sans-serif; }
.timestamp-badge { padding: 2px 6px; border-radius: 4px; font-weight: bold; }
.source-title { padding: 5px 10px; font-weight: bold; display: inline-block; border-radius: 4px; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

if "theme" not in st.session_state:
    st.session_state["theme"] = "Light"

if "history" not in st.session_state:
    st.session_state["history"] = []

if "active_video" not in st.session_state:
    st.session_state["active_video"] = None

def load_history():
    if os.path.exists("data/history.json"):
        with open("data/history.json", "r") as f:
            return json.load(f)
    return []

def save_history(history):
    os.makedirs("data", exist_ok=True)
    with open("data/history.json", "w") as f:
        json.dump(history, f)

st.session_state["history"] = load_history()

# Header
col1, col2 = st.columns([8, 1])
with col1:
    st.title("Lecture Query System")
    st.caption("Ask a question about your recorded lectures and get an instant, sourced answer.")
with col2:
    if st.button("🌙 Dark" if st.session_state["theme"] == "Light" else "☀️ Light"):
        st.session_state["theme"] = "Dark" if st.session_state["theme"] == "Light" else "Light"
        st.rerun()

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔒 Login Required")
        st.caption("Please log in to access the Lecture Query System.")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            if submit:
                if username == "admin" and password == "admin123":
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("Upload Lecture")
    uploaded_file = st.file_uploader("Upload a video or audio file", type=["mp4", "mp3", "m4a", "wav"])
    
    if uploaded_file is not None:
        if st.button("Transcribe & Process"):
            with st.spinner("Processing media... (this may take a while)"):
                os.makedirs("data/uploads", exist_ok=True)
                file_path = os.path.join("data/uploads", uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.info("Transcribing with Whisper...")
                transcript = transcribe(file_path)
                
                st.info("Saving to Vector Database...")
                save_transcript(transcript, uploaded_file.name)
                st.success("Ready! You can now query this lecture.")
                st.session_state["active_video"] = uploaded_file.name
                st.rerun()
                
    st.markdown("---")
    st.markdown("### Recordings")
    videos = list_videos()
    if videos:
        for v in videos:
            col_name, col_del = st.columns([4, 1], vertical_alignment="center")
            with col_name:
                if st.button(f"📹 {v}", key=f"sel_{v}"):
                    st.session_state["active_video"] = v
                    st.rerun()
            with col_del:
                if st.button("✖", key=f"del_{v}", help="Delete"):
                    delete_video(v)
                    if st.session_state["active_video"] == v:
                        st.session_state["active_video"] = None
                    st.rerun()
    else:
        st.caption("No recordings yet.")
        
    st.markdown("---")
    st.markdown("### Recent Queries")
    history = st.session_state.get("history", [])
    for item in history[-5:]:
        st.caption(f"Q: {item['question']}")

st.markdown("---")

if st.session_state["active_video"]:
    st.markdown(f"**Active Video:** `{st.session_state['active_video']}`")
    
    with st.form(key="query_form"):
        question = st.text_input("Ask anything about this lecture...")
        submit_button = st.form_submit_button(label="Ask")
        
    if submit_button and question:
        st.markdown("### Answer")
        stream, sources = ask(question, st.session_state["active_video"])
        
        answer_placeholder = st.empty()
        full_answer = ""
        for chunk in stream:
            full_answer += chunk
            answer_placeholder.markdown(full_answer + "▌")
        answer_placeholder.markdown(full_answer)
        
        if sources:
            st.markdown("---")
            st.markdown('<div class="source-title">Source Excerpts</div>', unsafe_allow_html=True)
            for src in sources:
                st.markdown(f'<span class="timestamp-badge">{src["timestamp"]}</span>', unsafe_allow_html=True)
                st.markdown(f"> {src['text']}")
                
        # Save to history
        history.append({"question": question, "answer": full_answer})
        save_history(history)
        st.session_state["history"] = history
else:
    st.info("Please select or upload a video from the sidebar to start querying.")
