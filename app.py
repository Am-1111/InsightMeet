import streamlit as st
import os
from backend.pipeline import run_pipeline

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="InsightMeet",
    page_icon="🎙️",
    layout="wide"
)

# ---------- SIDEBAR ----------
st.sidebar.title("🎛️ Controls")
dark_mode = st.sidebar.toggle("🌙 Dark Mode")
show_speakers = st.sidebar.checkbox("Show Speaker Diarization", value=True)

# ---------- THEME ----------
if dark_mode:
    st.markdown("""
    <style>
    body { background-color: #0e1117; color: #f0f6fc; }
    </style>
    """, unsafe_allow_html=True)

# ---------- HEADER ----------
st.title("🎙️ InsightMeet")
st.caption("AI-powered Meeting Intelligence Platform")

# ---------- FILE UPLOAD ----------
uploaded_file = st.file_uploader(
    "Upload meeting audio (mp3 / wav)",
    type=["mp3", "wav"]
)

if uploaded_file:
    os.makedirs("data/uploads", exist_ok=True)
    input_path = f"data/uploads/{uploaded_file.name}"

    with open(input_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("Audio uploaded successfully")

    if st.button("🚀 Analyze Meeting", use_container_width=True):

        with st.spinner("Processing meeting..."):
            output = run_pipeline(input_path)

        st.success("Analysis completed")

        # ---------- TABS ----------
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            ["📄 Transcript", "🗣️ Speakers", "📝 Summary", "✅ Action Items", "⚡ Impact Points"]
        )

        with tab1:
            st.text_area("Full Transcript", output["transcript"], height=350)

            st.download_button(
                "⬇️ Download Transcript",
                output["transcript"],
                file_name="transcript.txt"
            )

        with tab2:
            if show_speakers:
                st.text_area(
                    "Speaker-wise Transcript",
                    output["diarized_transcript"],
                    height=350
                )
            else:
                st.info("Enable speaker diarization from sidebar")

        with tab3:
            st.write(output["summary"])

        with tab4:
            if output["action_items"]:
                for item in output["action_items"]:
                    st.checkbox(item)
            else:
                st.info("No clear action items detected")
        
        

with tab5:
    for item in output["impact_points"]:
        st.markdown(
            f"**Score {item['score']}** — {item['sentence']}"
        )

