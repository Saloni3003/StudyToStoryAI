import gc
import torch
import streamlit as st


def release_models():

    # Clear Streamlit's cached model resources
    st.cache_resource.clear()

    gc.collect()

    if torch.backends.mps.is_available():
        torch.mps.empty_cache()

    if torch.cuda.is_available():
        torch.cuda.empty_cache()