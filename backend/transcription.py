import whisper
import os

# Prevent CPU overload
os.environ["OMP_NUM_THREADS"] = "1"

_MODEL = None


def get_model():
    global _MODEL
    if _MODEL is None:
        _MODEL = whisper.load_model("base")
    return _MODEL


def transcribe_audio(audio_path: str):
    """
    Transcribe audio using Whisper.
    Returns:
    - transcript (str)
    - segments (list of dicts)
    """
    model = get_model()
    result = model.transcribe(audio_path, fp16=False)

    transcript = result["text"]
    segments = result["segments"]

    return transcript, segments
