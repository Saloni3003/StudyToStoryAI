import os

from modules.extractor import extract_text
from modules.story_generator import generate_story
from modules.scene_parser import parse_scenes
from modules.image_generator import generate_image


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "input/GAN.pdf"

OUTPUT_DIR = "output/scenes"


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# STEP 1: EXTRACT STUDY MATERIAL
# ============================================================

print("\n")
print("=" * 70)
print("STEP 1: EXTRACTING STUDY MATERIAL")
print("=" * 70)

text = extract_text(INPUT_FILE)

print(f"\nExtracted characters: {len(text)}")


# ============================================================
# STEP 2: GENERATE STORYBOARD
# ============================================================

print("\n")
print("=" * 70)
print("STEP 2: GENERATING EDUCATIONAL STORYBOARD")
print("=" * 70)

story = generate_story(text)

print("Storyboard generated.")


# ============================================================
# STEP 3: PARSE STORYBOARD
# ============================================================

print("\n")
print("=" * 70)
print("STEP 3: PARSING STORYBOARD")
print("=" * 70)

parsed = parse_scenes(story)

scenes = parsed["scenes"]

print(f"Title: {parsed['title']}")
print(f"Number of scenes: {len(scenes)}")


# ============================================================
# VALIDATION
# ============================================================

if len(scenes) != 6:

    raise ValueError(
        f"Expected 6 scenes, but found {len(scenes)}."
    )


# ============================================================
# STEP 4: GENERATE IMAGES
# ============================================================

print("\n")
print("=" * 70)
print("STEP 4: GENERATING SCENE IMAGES")
print("=" * 70)


for scene in scenes:

    scene_number = scene["scene_number"]

    visual = scene["visual"]

    technical_concept = scene["technical_concept"]

    print("\n" + "-" * 70)

    print(f"Generating Scene {scene_number}")

    print(f"Technical Concept: {technical_concept}")

    print(f"Visual: {visual}")

    # --------------------------------------------------------
    # Create a controlled image prompt
    # --------------------------------------------------------

    prompt = f"""
Photorealistic cinematic educational scene.

Topic:
{technical_concept}

Visual:
{visual}

Style:
modern university educational video,
realistic people and technology,
natural lighting,
professional documentary photography,
cinematic composition,
16:9 widescreen,
high detail.

The image should visually explain the educational concept.

Do not include:
text,
labels,
logos,
watermarks,
captions,
cartoon style,
anime,
illustration,
painting.
"""

    output_path = os.path.join(
        OUTPUT_DIR,
        f"scene_{scene_number}.png"
    )

    # --------------------------------------------------------
    # Generate image
    # --------------------------------------------------------

    generate_image(
        prompt,
        output_path,
        seed=100 + scene_number
    )

    print(
        f"Scene {scene_number} image saved:"
        f" {output_path}"
    )


# ============================================================
# COMPLETE
# ============================================================

print("\n")
print("=" * 70)
print("IMAGE GENERATION COMPLETED")
print("=" * 70)

print("\nGenerated images:")

for scene in scenes:

    path = os.path.join(
        OUTPUT_DIR,
        f"scene_{scene['scene_number']}.png"
    )

    print(path)

print("\n")
print("Next step: visually inspect the six generated images.")