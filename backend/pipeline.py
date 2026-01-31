from backend.audio_processing import preprocess_audio
from backend.transcription import transcribe_with_segments
from backend.diarization import diarize_transcript
from backend.summarization import summarize_text
from backend.action_items import extract_action_items

def run_pipeline(audio_path: str) -> dict:
    cleaned_audio = preprocess_audio(
        audio_path,
        "data/uploads/cleaned_meeting.wav"
    )

    transcript, segments = transcribe_with_segments(cleaned_audio)
    diarized = diarize_transcript(segments)
    summary = summarize_text(transcript)
    actions = extract_action_items(transcript)

    return {
        "transcript": transcript,
        "diarized_transcript": diarized,
        "summary": summary,
        "action_items": actions
    }
