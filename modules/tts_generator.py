import os
import streamlit as st
from kokoro import KPipeline
import soundfile as sf


# ============================================================
# KOKORO CONFIGURATION
# ============================================================

VOICE = "af_heart"
LANGUAGE = "a"


# ============================================================
# LOAD KOKORO
# ============================================================

@st.cache_resource
def load_kokoro():

    print("Loading Kokoro TTS...")

    pipeline = KPipeline(
        lang_code=LANGUAGE
    )

    return pipeline


# ============================================================
# GENERATE TTS
# ============================================================

def generate_tts(text, output_path):

    if not text or not text.strip():
        raise ValueError(
            "Cannot generate narration because the text is empty."
        )

    pipeline = load_kokoro()

    output_directory = os.path.dirname(output_path)

    if output_directory:
        os.makedirs(
            output_directory,
            exist_ok=True
        )

    print("\nGenerating Kokoro narration...")
    print(f"Text: {text}")

    # --------------------------------------------------------
    # Generate speech
    # --------------------------------------------------------

    generator = pipeline(
        text,
        voice=VOICE
    )

    audio_chunks = []

    for _, _, audio in generator:

        audio_chunks.append(audio)

    if not audio_chunks:
        raise RuntimeError(
            "Kokoro did not generate any audio."
        )

    # --------------------------------------------------------
    # Combine audio chunks
    # --------------------------------------------------------

    import numpy as np

    audio = np.concatenate(
        audio_chunks
    )

    # --------------------------------------------------------
    # Save WAV
    # --------------------------------------------------------

    sf.write(
        output_path,
        audio,
        24000
    )

    print(
        f"Kokoro narration saved: {output_path}"
    )

    return output_path