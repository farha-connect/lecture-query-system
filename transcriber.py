import whisper
import os

def transcribe(video_path):
    """
    Transcribes the given video/audio file using a local Whisper model.
    Returns the full transcription with timestamps.
    """
    # Load the base Whisper model. It's downloaded to ~/.cache/whisper on first run.
    # You can change to 'tiny' for speed, or 'small'/'medium' for better accuracy.
    model = whisper.load_model("base")
    
    # Run the transcription with word-level timestamps (optional, but helpful for search)
    result = model.transcribe(video_path)
    
    return result
