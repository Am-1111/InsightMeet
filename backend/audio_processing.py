import subprocess
import os

def preprocess_audio(input_audio_path: str, output_audio_path: str) -> str:
    """
    STEP 1: Audio preprocessing
    (pydub-equivalent using FFmpeg, Python 3.13 safe)
    """

    os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_audio_path,
        "-ac", "1",
        "-ar", "16000",
        "-af", "loudnorm",
        output_audio_path
    ]

    subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )

    return output_audio_path
