from modules.extractor import extract_text
from modules.story_generator import generate_story
from modules.scene_parser import parse_scenes


# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = "Untitled document.pdf"


# ============================================================
# EXTRACT STUDY MATERIAL
# ============================================================

print("\n")
print("=" * 70)
print("EXTRACTING STUDY MATERIAL")
print("=" * 70)

text = extract_text(INPUT_FILE)

print("\nExtracted characters:", len(text))

print("\nSource material:")
print("-" * 70)
print(text)
print("-" * 70)


# ============================================================
# GENERATE STORYBOARD
# ============================================================

print("\n")
print("=" * 70)
print("GENERATING EDUCATIONAL STORYBOARD")
print("=" * 70)

story = generate_story(text)


# ============================================================
# DISPLAY RAW STORYBOARD
# ============================================================

print("\n")
print("=" * 70)
print("GENERATED STORYBOARD")
print("=" * 70)

print(story)


# ============================================================
# PARSE STORYBOARD
# ============================================================

print("\n")
print("=" * 70)
print("PARSING STORYBOARD")
print("=" * 70)

parsed = parse_scenes(story)


# ============================================================
# DISPLAY PARSED RESULT
# ============================================================

print("\nTitle:")
print(parsed["title"])

print("\nNumber of scenes:")
print(len(parsed["scenes"]))


for scene in parsed["scenes"]:

    print("\n" + "-" * 70)

    print(f"Scene {scene['scene_number']}")

    print("\nNarration:")
    print(scene["narration"])

    print("\nVisual:")
    print(scene["visual"])

    print("\nAnimation:")
    print(scene["animation"])

    print("\nTechnical Concept:")
    print(scene["technical_concept"])

    print("\nTransition:")
    print(scene["transition"])


# ============================================================
# VALIDATION
# ============================================================

print("\n")
print("=" * 70)
print("VALIDATION")
print("=" * 70)

if len(parsed["scenes"]) == 6:
    print("SUCCESS: Exactly 6 scenes were parsed.")
else:
    print(
        f"WARNING: Expected 6 scenes, "
        f"but found {len(parsed['scenes'])}."
    )

for scene in parsed["scenes"]:

    required_fields = [
        "narration",
        "visual",
        "animation",
        "technical_concept",
        "transition"
    ]

    missing = [
        field
        for field in required_fields
        if not scene[field]
    ]

    if missing:
        print(
            f"Scene {scene['scene_number']} "
            f"missing: {missing}"
        )
    else:
        print(
            f"Scene {scene['scene_number']}: "
            f"OK"
        )

print("\n")
print("=" * 70)
print("TEST COMPLETED")
print("=" * 70)