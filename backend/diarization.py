def diarize_transcript(segments):
    """
    Simple speaker diarization based on time gaps.
    Output: [{speaker, text}]
    """

    diarized = []
    speaker_id = 1
    last_end = 0.0

    for seg in segments:
        start = seg["start"]

        # New speaker if long pause
        if start - last_end > 1.5:
            speaker_id += 1

        diarized.append({
            "speaker": f"Speaker {speaker_id}",
            "text": seg["text"].strip()
        })

        last_end = seg["end"]

    return diarized
