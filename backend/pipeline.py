from backend.audio_processing import preprocess_audio
from backend.transcription import transcribe_audio
from backend.summarization import summarize_text
from backend.impact_score import extract_impact_points
from backend.recap_engine import generate_recap
from backend.database import save_meeting, fetch_previous_summaries
from backend.diarization import diarize_transcript




def run_pipeline(audio_path: str) -> dict:
    """
    End-to-end meeting processing pipeline
    """

    # 1️⃣ Preprocess audio
    cleaned_path = audio_path.replace(".mp3", "_cleaned.wav")
    preprocess_audio(audio_path, cleaned_path)

    # 2️⃣ Transcription
    transcript, segments = transcribe_audio(cleaned_path)

    # 3️⃣ Summarization
    summary = summarize_text(transcript)

    # 4️⃣ Fetch previous meetings
    previous = fetch_previous_summaries(limit=5)

    # 5️⃣ Generate recap
    recap = generate_recap(previous, summary)

    # 6️⃣ Impact points
    impact_points = extract_impact_points(transcript)

    # 7️⃣ Save meeting
    save_meeting(
        title="Project Meeting",
        transcript=transcript,
        summary=summary
    )
    

    return {
        "transcript": transcript,
        "summary": summary,
        "recap": recap,
        "impact_points": impact_points,
        "segments": segments
    }
