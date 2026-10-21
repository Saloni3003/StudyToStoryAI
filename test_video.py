import os
import shutil

from modules.extractor import extract_text
from modules.story_generator import generate_story
from modules.scene_parser import parse_scenes
from modules.image_generator import generate_image
from modules.tts_generator import generate_tts

from modules.video_generator import create_final_video


# ==========================================================
# CONFIGURATION
# ==========================================================

INPUT_FILE = "input/GAN.pdf"

OUTPUT_DIR = "output"

SCENE_IMAGE_DIR = os.path.join(
    OUTPUT_DIR,
    "scenes"
)

AUDIO_DIR = os.path.join(
    OUTPUT_DIR,
    "audio"
)

VIDEO_DIR = os.path.join(
    OUTPUT_DIR,
    "video"
)

FINAL_VIDEO = os.path.join(
    OUTPUT_DIR,
    "StudyToStory_final.mp4"
)


# ==========================================================
# PIPELINE START
# ==========================================================

print("\n" + "=" * 70)
print("STUDYTOSTORY AI - COMPLETE PIPELINE")
print("=" * 70)


# ==========================================================
# PREPARE OUTPUT DIRECTORIES
# ==========================================================

print("\nPreparing output directories...")

os.makedirs(
    SCENE_IMAGE_DIR,
    exist_ok=True
)

os.makedirs(
    AUDIO_DIR,
    exist_ok=True
)

os.makedirs(
    VIDEO_DIR,
    exist_ok=True
)


# Remove only previous final video.
# Keep existing scene images because SDXL generation is expensive.

if os.path.exists(FINAL_VIDEO):

    print("\nRemoving previous final video...")

    os.remove(
        FINAL_VIDEO
    )


# ==========================================================
# STEP 1: EXTRACT TEXT
# ==========================================================

print("\n" + "=" * 70)
print("STEP 1: EXTRACTING STUDY MATERIAL")
print("=" * 70)

if not os.path.exists(INPUT_FILE):

    raise FileNotFoundError(
        f"Input file not found: {INPUT_FILE}"
    )


source_text = extract_text(
    INPUT_FILE
)

if not source_text.strip():

    raise ValueError(
        "No text could be extracted from the input file."
    )


print("\nExtracted text:")
print("-" * 70)
print(source_text[:1500])

print("\nExtracted characters:", len(source_text))


# ==========================================================
# STEP 2: GENERATE STORYBOARD
# ==========================================================

print("\n" + "=" * 70)
print("STEP 2: GENERATING EDUCATIONAL STORYBOARD")
print("=" * 70)

storyboard_text = generate_story(
    source_text
)

print("\nGenerated Storyboard:")
print("-" * 70)
print(storyboard_text)


# ==========================================================
# STEP 3: PARSE STORYBOARD
# ==========================================================

print("\n" + "=" * 70)
print("STEP 3: PARSING STORYBOARD")
print("=" * 70)

storyboard = parse_scenes(
    storyboard_text
)

title = storyboard.get(
    "title",
    "StudyToStory AI"
)

scenes = storyboard.get(
    "scenes",
    []
)

print("\nTitle:")
print(title)

print("\nNumber of scenes:", len(scenes))


if len(scenes) != 6:

    raise ValueError(
        f"Expected 6 scenes, but found {len(scenes)}."
    )


# ==========================================================
# DISPLAY PARSED SCENES
# ==========================================================

for scene in scenes:

    print("\n" + "-" * 70)

    print(
        f"SCENE {scene['scene_number']}"
    )

    print(
        "Narration:",
        scene["narration"]
    )

    print(
        "Visual:",
        scene["visual"]
    )

    print(
        "Animation:",
        scene["animation"]
    )

    print(
        "Technical Concept:",
        scene["technical_concept"]
    )

    print(
        "Transition:",
        scene["transition"]
    )


# ==========================================================
# STEP 4: GENERATE / REUSE SCENE IMAGES
# ==========================================================

print("\n" + "=" * 70)
print("STEP 4: GENERATING / REUSING SCENE IMAGES")
print("=" * 70)

image_paths = []


for scene in scenes:

    scene_number = scene[
        "scene_number"
    ]

    visual = scene[
        "visual"
    ]

    image_path = os.path.join(
        SCENE_IMAGE_DIR,
        f"scene_{scene_number}.png"
    )

    # ------------------------------------------------------
    # Reuse existing image
    # ------------------------------------------------------

    if os.path.exists(image_path):

        print(
            f"\nScene {scene_number}: "
            f"existing image found — reusing it."
        )

    else:

        print(
            f"\nGenerating image for Scene {scene_number}..."
        )

        prompt = (
            "Photorealistic educational documentary scene, "
            "modern university environment, "
            f"{visual}, "
            "realistic people and technology, "
            "natural lighting, cinematic photography, "
            "16:9 widescreen composition, "
            "high detail, "
            "no text, no logos, no watermark"
        )

        print(
            "Prompt:",
            prompt
        )

        generate_image(
            prompt,
            image_path,
            seed=42 + scene_number
        )

        print(
            f"Scene {scene_number} image generated."
        )

    image_paths.append(
        image_path
    )


# ==========================================================
# VERIFY IMAGES
# ==========================================================

print("\n" + "=" * 70)
print("VERIFYING SCENE IMAGES")
print("=" * 70)

for image_path in image_paths:

    if not os.path.exists(image_path):

        raise FileNotFoundError(
            f"Image was not generated: {image_path}"
        )

    print(
        "✓",
        image_path
    )


# ==========================================================
# STEP 5: GENERATE / REUSE KOKORO AUDIO
# ==========================================================

print("\n" + "=" * 70)
print("STEP 5: GENERATING / REUSING KOKORO NARRATION")
print("=" * 70)

audio_paths = []


for scene in scenes:

    scene_number = scene[
        "scene_number"
    ]

    narration = scene[
        "narration"
    ]

    audio_path = os.path.join(
        AUDIO_DIR,
        f"scene_{scene_number}.wav"
    )

    # ------------------------------------------------------
    # Generate audio if it does not already exist
    # ------------------------------------------------------

    if os.path.exists(audio_path):

        print(
            f"\nScene {scene_number}: "
            f"existing audio found — reusing it."
        )

    else:

        print(
            f"\nGenerating narration "
            f"for Scene {scene_number}..."
        )

        print(
            "Narration:",
            narration
        )

        generate_tts(
            narration,
            audio_path
        )

        print(
            f"Scene {scene_number} audio generated."
        )

    audio_paths.append(
        audio_path
    )


# ==========================================================
# VERIFY AUDIO
# ==========================================================

print("\n" + "=" * 70)
print("VERIFYING AUDIO FILES")
print("=" * 70)

for audio_path in audio_paths:

    if not os.path.exists(audio_path):

        raise FileNotFoundError(
            f"Audio was not generated: {audio_path}"
        )

    print(
        "✓",
        audio_path
    )


# ==========================================================
# STEP 6: CREATE FINAL VIDEO
# ==========================================================

print("\n" + "=" * 70)
print("STEP 6: CREATING FINAL VIDEO")
print("=" * 70)

print("\nTitle:")
print(title)

print("\nImages:", len(image_paths))

print("Audio files:", len(audio_paths))

print(
    "\nCreating title card, animated scenes, "
    "adding narration and combining everything..."
)


create_final_video(
    image_paths=image_paths,
    audio_paths=audio_paths,
    output_path=FINAL_VIDEO,
    title=title
)


# ==========================================================
# STEP 7: VERIFY FINAL VIDEO
# ==========================================================

print("\n" + "=" * 70)
print("STEP 7: VERIFYING FINAL VIDEO")
print("=" * 70)

if not os.path.exists(FINAL_VIDEO):

    raise FileNotFoundError(
        "Final video was not created."
    )


file_size = os.path.getsize(
    FINAL_VIDEO
)

print(
    "\n✓ FINAL VIDEO CREATED SUCCESSFULLY"
)

print(
    "\nOutput:",
    FINAL_VIDEO
)

print(
    "File size:",
    round(
        file_size / (1024 * 1024),
        2
    ),
    "MB"
)


# ==========================================================
# COMPLETE
# ==========================================================

print("\n" + "=" * 70)
print("STUDYTOSTORY AI PIPELINE COMPLETE")
print("=" * 70)

print("\nPipeline:")
print("Study Material")
print("      ↓")
print("Text Extraction")
print("      ↓")
print("Qwen2.5-3B-Instruct")
print("      ↓")
print("Educational Storyboard")
print("      ↓")
print("6 Scene Parser")
print("      ↓")
print(" ┌───────────────┬───────────────┐")
print(" ↓               ↓")
print("SDXL-Turbo       Kokoro TTS")
print(" ↓               ↓")
print("Scene Images     Narration")
print(" └───────────────┴───────────────┘")
print("              ↓")
print("     Animated Video Scenes")
print("              ↓")
print("        Final MP4 Video")
print("              ↓")
print("   StudyToStory_final.mp4")

print("\nFinal output:")
print(FINAL_VIDEO)

print("\n" + "=" * 70)