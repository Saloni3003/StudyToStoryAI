import os
import torch
import streamlit as st
from diffusers import AutoPipelineForText2Image

MODEL_NAME = "stabilityai/sdxl-turbo"


if torch.backends.mps.is_available():
    DEVICE = "mps"
elif torch.cuda.is_available():
    DEVICE = "cuda"
else:
    DEVICE = "cpu"


@st.cache_resource
def load_image_model():

    st.info(f"Loading SDXL-Turbo on: {DEVICE}")

    pipe = AutoPipelineForText2Image.from_pretrained(
        MODEL_NAME,
        dtype=torch.float16,
        variant="fp16"
    )

    pipe = pipe.to(DEVICE)

    # Important for SDXL on Apple Silicon
    # Do NOT enable attention slicing.

    return pipe


def generate_image(prompt, output_path, seed=42):
    pipe = load_image_model()

    # Keep the prompt short because SDXL's CLIP text encoder
    # has a limited token length.
    prompt = prompt.strip()

    if DEVICE == "mps":
        generator = torch.Generator(device="cpu").manual_seed(seed)
    else:
        generator = torch.Generator(device=DEVICE).manual_seed(seed)

    result = pipe(
        prompt=prompt,
        height=576,
        width=1024,
        num_inference_steps=4,
        guidance_scale=0.0,
        generator=generator
    )

    image = result.images[0]

    output_directory = os.path.dirname(output_path)

    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    image.save(output_path)

    return output_path