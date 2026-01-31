def diarize_transcript(segments):
    """
    STEP: Speaker Diarization (heuristic-based, Python 3.13 safe)

    Input: Whisper segments
    Output: Speaker-labeled transcript
    """

    diarized_text = []
    current_speaker = 1

    for i, seg in enumerate(segments):
        # Simple speaker switch heuristic
        if i > 0 and seg["start"] - segments[i-1]["end"] > 1.0:
            current_speaker += 1

        diarized_text.append(
            f"Speaker {current_speaker}: {seg['text'].strip()}"
        )

    return "\n".join(diarized_text)
