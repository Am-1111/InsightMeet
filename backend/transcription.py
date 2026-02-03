import whisper

_MODEL = whisper.load_model("base")   


def transcribe_with_segments(audio_path):
    result = _MODEL.transcribe(
        audio_path,
        fp16=False,
        verbose=False
    )
    return result["text"], result["segments"]
