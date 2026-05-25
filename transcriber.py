import whisper
import os

def transcribe(video_path):
    """
    Transcribes the given video/audio file using a local Whisper model.
    Returns the full transcription with timestamps.
    """
    
    model = whisper.load_model("base")
    
    
    result = model.transcribe(video_path)
    
    return result
