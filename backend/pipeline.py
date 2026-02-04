from backend.audio_processing import preprocess_audio
from backend.transcription import transcribe_audio
from backend.summarization import summarize_text
from backend.impact_score import extract_impact_points
from backend.recap_engine import generate_recap
from backend.database import save_meeting, fetch_previous_summaries
from backend.diarization import diarize_transcript



def run_pipeline(audio_path: str, status_callback=None):

    def update(msg):
        if status_callback:
            status_callback(msg)

    update("🔊 Preprocessing audio...")
    cleaned_path = audio_path.replace(".mp3", "_cleaned.wav")
    preprocess_audio(audio_path, cleaned_path)

    update("📝 Transcribing speech...")
    transcript, segments = transcribe_audio(cleaned_path)

    update("🧠 Generating summary...")
    summary = summarize_text(transcript)

    update("🔁 Fetching previous meetings...")
    previous = fetch_previous_summaries(limit=5)

    update("📌 Generating recap...")
    recap = generate_recap(previous, summary)

    update("⭐ Extracting impact points...")
    impact_points = extract_impact_points(transcript)

    update("💾 Saving meeting...")
    save_meeting("Project Meeting", transcript, summary)

    update("✅ Completed")

    return {
        "transcript": transcript,
        "summary": summary,
        "recap": recap,
        "impact_points": impact_points
    }
