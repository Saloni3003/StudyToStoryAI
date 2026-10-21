import os
import shutil
import streamlit as st

from modules.extractor import extract_text
from modules.story_generator import generate_story
from modules.scene_parser import parse_scenes
from modules.image_generator import generate_image
from modules.tts_generator import generate_tts
from modules.video_generator import create_final_video


# ==========================================================
# CONFIGURATION
# ==========================================================

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
# STREAMLIT PAGE
# ==========================================================

st.set_page_config(
    page_title="StudyToStory AI",
    page_icon="🎬",
    layout="wide"
)


# ==========================================================
# HEADER
# ==========================================================

st.title("🎬 StudyToStory AI")

st.markdown(
    """
    ### Transform Study Material into an AI-Generated Educational Video

    Upload your study material and let AI transform it into:

    **Study Material → Educational Story → Scene Images → Narration → Video**
    """
)

st.divider()


# ==========================================================
# FILE UPLOAD
# ==========================================================

st.header("📄 Upload Study Material")

uploaded_file = st.file_uploader(
    "Upload a PDF or image",
    type=["pdf", "png", "jpg", "jpeg"]
)


# ==========================================================
# GENERATION
# ==========================================================

if uploaded_file is not None:

    st.success(
        f"Uploaded file: {uploaded_file.name}"
    )

    generate_button = st.button(
        "🚀 Generate Educational Video",
        type="primary"
    )

    if generate_button:

        # ==================================================
        # CREATE DIRECTORIES
        # ==================================================

        os.makedirs(
            OUTPUT_DIR,
            exist_ok=True
        )

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


        # ==================================================
        # SAVE UPLOADED FILE
        # ==================================================

        input_dir = "input"

        os.makedirs(
            input_dir,
            exist_ok=True
        )

        input_path = os.path.join(
            input_dir,
            uploaded_file.name
        )

        with open(
            input_path,
            "wb"
        ) as file:

            file.write(
                uploaded_file.getbuffer()
            )


        # ==================================================
        # CLEAN PREVIOUS OUTPUT
        # ==================================================

        for directory in [
            SCENE_IMAGE_DIR,
            AUDIO_DIR,
            VIDEO_DIR
        ]:

            if os.path.exists(directory):

                shutil.rmtree(
                    directory
                )

            os.makedirs(
                directory,
                exist_ok=True
            )


        if os.path.exists(
            FINAL_VIDEO
        ):

            os.remove(
                FINAL_VIDEO
            )


        # ==================================================
        # PROGRESS BAR
        # ==================================================

        progress = st.progress(
            0
        )


        # ==================================================
        # STEP 1
        # TEXT EXTRACTION
        # ==================================================

        st.header(
            "1️⃣ Extracting Study Material"
        )

        with st.spinner(
            "Extracting text from your study material..."
        ):

            source_text = extract_text(
                input_path
            )

        if not source_text.strip():

            st.error(
                "❌ No text could be extracted from the uploaded file."
            )

            st.stop()

        st.success(
            "✅ Study material extracted successfully."
        )

        with st.expander(
            "📖 View Extracted Text"
        ):

            st.write(
                source_text
            )

        progress.progress(
            15
        )


        # ==================================================
        # STEP 2
        # STORY GENERATION
        # ==================================================

        st.header(
            "2️⃣ Generating Educational Story"
        )

        with st.spinner(
            "Qwen2.5-3B-Instruct is generating the educational storyboard..."
        ):

            storyboard_text = generate_story(
                source_text
            )

        st.success(
            "✅ Educational storyboard generated."
        )

        with st.expander(
            "🎬 View Generated Storyboard"
        ):

            st.text(
                storyboard_text
            )

        progress.progress(
            30
        )


        # ==================================================
        # STEP 3
        # SCENE PARSING
        # ==================================================

        st.header(
            "3️⃣ Preparing Educational Scenes"
        )

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

        if not scenes:

            st.error(
                "❌ No scenes were detected."
            )

            st.stop()

        st.success(
            f"✅ {len(scenes)} scenes prepared."
        )

        for scene in scenes:

            with st.expander(
                f"🎞️ Scene {scene['scene_number']}"
            ):

                st.write(
                    "**Narration:**"
                )

                st.write(
                    scene["narration"]
                )

                st.write(
                    "**Visual:**"
                )

                st.write(
                    scene["visual"]
                )

                st.write(
                    "**Technical Concept:**"
                )

                st.write(
                    scene["technical_concept"]
                )

        progress.progress(
            40
        )


        # ==================================================
        # STEP 4
        # IMAGE GENERATION
        # ==================================================

        st.header(
            "4️⃣ Generating Scene Images"
        )

        image_paths = []

        image_progress = st.progress(
            0
        )

        for index, scene in enumerate(
            scenes
        ):

            scene_number = scene[
                "scene_number"
            ]

            st.write(
                f"🖼️ Generating Scene {scene_number}..."
            )

            image_path = os.path.join(
                SCENE_IMAGE_DIR,
                f"scene_{scene_number}.png"
            )

            prompt = (
                "Photorealistic educational documentary scene, "
                "modern university environment, "
                f"{scene['visual']}, "
                "realistic people and technology, "
                "natural lighting, cinematic photography, "
                "16:9 widescreen composition, "
                "high detail, "
                "no text, no logos, no watermark"
            )

            generate_image(
                prompt,
                image_path,
                seed=42 + scene_number
            )

            image_paths.append(
                image_path
            )

            image_progress.progress(
                (index + 1) / len(scenes)
            )


        st.success(
            "✅ All scene images generated."
        )


        # ==================================================
        # DISPLAY IMAGES
        # ==================================================

        st.subheader(
            "🖼️ Generated Scene Images"
        )

        for index, image_path in enumerate(
            image_paths
        ):

            col1, col2 = st.columns(
                2
            )

            with col1:

                st.image(
                    image_path,
                    caption=f"Scene {index + 1}"
                )

            with col2:

                scene = scenes[index]

                st.markdown(
                    f"### Scene {index + 1}"
                )

                st.write(
                    scene["technical_concept"]
                )

                st.write(
                    scene["narration"]
                )


        progress.progress(
            60
        )


        # ==================================================
        # STEP 5
        # KOKORO NARRATION
        # ==================================================

        st.header(
            "5️⃣ Generating AI Narration"
        )

        audio_paths = []

        audio_progress = st.progress(
            0
        )

        for index, scene in enumerate(
            scenes
        ):

            scene_number = scene[
                "scene_number"
            ]

            audio_path = os.path.join(
                AUDIO_DIR,
                f"scene_{scene_number}.wav"
            )

            st.write(
                f"🔊 Generating narration for Scene {scene_number}..."
            )

            generate_tts(
                scene["narration"],
                audio_path
            )

            audio_paths.append(
                audio_path
            )

            audio_progress.progress(
                (index + 1) / len(scenes)
            )


        st.success(
            "✅ Kokoro narration generated."
        )

        progress.progress(
            75
        )


        # ==================================================
        # STEP 6
        # VIDEO GENERATION
        # ==================================================

        st.header(
            "6️⃣ Creating Final Educational Video"
        )

        with st.spinner(
            "Combining images, narration and animations..."
        ):

            create_final_video(
                image_paths=image_paths,
                audio_paths=audio_paths,
                output_path=FINAL_VIDEO,
                title=title
            )

        if not os.path.exists(
            FINAL_VIDEO
        ):

            st.error(
                "❌ Final video was not created."
            )

            st.stop()


        progress.progress(
            100
        )

        st.success(
            "🎉 Final educational video generated successfully!"
        )


        # ==================================================
        # DISPLAY FINAL VIDEO
        # ==================================================

        st.divider()

        st.header(
            "🎬 Your Generated Educational Video"
        )

        st.video(
            FINAL_VIDEO
        )


        # ==================================================
        # DOWNLOAD
        # ==================================================

        with open(
            FINAL_VIDEO,
            "rb"
        ) as video_file:

            st.download_button(
                "⬇️ Download Generated Video",
                video_file,
                file_name="StudyToStory_final.mp4",
                mime="video/mp4"
            )


        # ==================================================
        # COMPLETION
        # ==================================================

        st.divider()

        st.success(
            """
            ✅ StudyToStory AI pipeline completed!

            Study Material → Text Extraction → Qwen Storyboard →
            SDXL-Turbo Images → Kokoro Narration → Final Video
            """
        )


else:

    st.info(
        "👆 Upload your study material above to start."
    )