import whisper

_MODEL = None

def get_model():
    """
    Lazy-load Whisper model (loads only once)
    """
    global _MODEL
    if _MODEL is None:
        print("🔄 Loading Whisper model (small)...")
        _MODEL = whisper.load_model("small")  # FAST + GOOD QUALITY
    return _MODEL


def transcribe_audio(audio_path: str):
    model = get_model()

    result = model.transcribe(audio_path)

    transcript = result["text"]
    segments = result.get("segments", [])

    return transcript, segments
