from typing import Any

import streamlit as st


def image(label: str = 'Please upload an image.') -> Any | None:
    image = st.file_uploader(
        label=label,
        type=['jpg', 'jpeg', 'png'],
    )

    if image is not None:
        st.image(image)
    return image


def webcam(label: str = 'Please attach your webcam.') -> Any | None:
    image = st.camera_input(
        label=label,
    )

    if image is not None:
        st.image(image)
    return image
