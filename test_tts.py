from modules.tts_generator import generate_tts


text = """
GANs are models that generate new, realistic data
by learning from existing data.
"""


output_path = "output/test_kokoro.wav"


print("\n")
print("=" * 70)
print("TESTING KOKORO TTS")
print("=" * 70)

generate_tts(
    text,
    output_path
)

print("\n")
print("=" * 70)
print("TTS TEST COMPLETED")
print("=" * 70)

print(f"\nAudio file: {output_path}")