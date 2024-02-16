from typing import Any

import streamlit as st


def any_image() -> Any | None:
    col_webcam, col_file = st.tabs(['Webcam', 'File'])
    with col_webcam:
        img = webcam()
    with col_file:
        img = img or image()
    return img


def image(label: str = 'Please upload an image.', display: bool = True) -> Any | None:
    image = st.file_uploader(
        label=label,
        type=['jpg', 'jpeg', 'png'],
    )

    if display and image is not None:
        st.image(image)
    return image


def webcam(label: str = 'Please attach your webcam.', display: bool = False) -> Any | None:
    image = st.camera_input(
        label=label,
    )

    if display and image is not None:
        st.image(image)
    return image
