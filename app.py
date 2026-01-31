import streamlit as st
import os

from backend.audio_processing import preprocess_audio
from backend.transcription import transcribe_with_segments
from backend.diarization import diarize_transcript
from backend.summarization import summarize_text
from backend.action_items import extract_action_items
from backend.impact_score import run_impact_score

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="InsightMeet",
    page_icon="🎙️",
    layout="wide"
)

st.title("🎙️ InsightMeet")
st.caption("On-demand AI Meeting Intelligence (CPU Optimized)")

# ---------------- SESSION STATE ----------------
for key in [
    "audio_path", "cleaned_audio",
    "transcript", "segments",
    "diarized", "summary",
    "actions", "impact"
]:
    if key not in st.session_state:
        st.session_state[key] = None

# ---------------- UPLOAD ----------------
uploaded_file = st.file_uploader(
    "Upload meeting audio (mp3 / wav)",
    type=["mp3", "wav"]
)

if uploaded_file:
    os.makedirs("data/uploads", exist_ok=True)
    audio_path = f"data/uploads/{uploaded_file.name}"

    with open(audio_path, "wb") as f:
        f.write(uploaded_file.read())

    st.session_state.audio_path = audio_path
    st.success("Audio uploaded successfully")

# ---------------- LAYOUT ----------------
left, right = st.columns([1, 2])

# ================= LEFT: CONTROLS =================
with left:
    st.subheader("⚙️ Run Models")

    # STEP 1
    if st.button("🎧 Run Audio Preprocessing"):
        st.session_state.cleaned_audio = preprocess_audio(
            st.session_state.audio_path,
            "data/uploads/cleaned_meeting.wav"
        )
        st.success("Preprocessing done")

    # STEP 2
    if st.button("🧠 Run Transcription (Whisper)"):
        transcript, segments = transcribe_with_segments(
            st.session_state.cleaned_audio
        )
        st.session_state.transcript = transcript
        st.session_state.segments = segments
        st.success("Transcription done")

    # STEP 3
    if st.button("🗣️ Run Speaker Diarization"):
        st.session_state.diarized = diarize_transcript(
            st.session_state.segments
        )
        st.success("Diarization done")

    # STEP 4
    if st.button("📝 Run Summarization (BART)"):
        st.session_state.summary = summarize_text(
            st.session_state.transcript
        )
        st.success("Summary generated")

    # STEP 5
    if st.button("✅ Extract Action Items"):
        st.session_state.actions = extract_action_items(
            st.session_state.transcript
        )
        st.success("Action items extracted")

    # STEP 6
    if st.button("⭐ Run IMPACTScore™"):
        st.session_state.impact = run_impact_score(
            st.session_state.transcript
        )
        st.success("Key insights ranked")

# ================= RIGHT: OUTPUT =================
with right:
    st.subheader("📊 Results")

    tabs = st.tabs([
        "📄 Transcript",
        "🗣️ Speakers",
        "📝 Summary",
        "✅ Actions",
        "⭐ Key Insights"
    ])

    with tabs[0]:
        st.text_area(
            "Transcript",
            st.session_state.transcript or "",
            height=300
        )

    with tabs[1]:
        st.text_area(
            "Speaker-wise Transcript",
            st.session_state.diarized or "",
            height=300
        )

    with tabs[2]:
        st.write(st.session_state.summary or "Not generated yet")

    with tabs[3]:
        if st.session_state.actions:
            for item in st.session_state.actions:
                st.checkbox(item)
        else:
            st.info("No action items yet")

    with tabs[4]:
        if st.session_state.impact:
            for item in st.session_state.impact:
                st.markdown(
                    f"**Score {item['score']}** — {item['sentence']}"
                )
        else:
            st.info("Run IMPACTScore™ to see key insights")
