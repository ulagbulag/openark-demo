import asyncio
from typing import Any

import av
import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer

from utils import code, upload


async def get_inputs() -> dict[str, Any]:
    return {}


async def execute() -> None:

    async def queued_video_frames_callback(frames):
        # 0. Check inputs
        imgs = [
            frame.to_ndarray(format='bgr24')
            for frame in frames
        ]

        image_name: str = 'img.jpg'
        image_data = cv2.imencode('.jpg', imgs[-1])[1].tobytes()

        # 1. Import needed libraries
        from openark import OpenArk

        # 2. Create an OpenARK instance
        ark = OpenArk.cloned()

        # 3. Define the Image Classification function
        function_name = 'image-classification'

        # 4. Load the function
        function = await ark.get_function(function_name)

        # 5. Make input payloads
        input_payloads = {
            image_name: image_data,
        }

        # 6. Make an input value
        input_value = {
            # NOTE: the prefix "@data:image" describes that this payload data is an image.
            'images': [
                f'@data:image,{image_name}',
            ],
        }

        # 7. Call the function and return the output message
        input_message = await function(
            value=input_value,
            payloads=input_payloads,
        )

        # 8. Find the results
        image_objects = input_message['value']

        # 9. Render labels
        for idx, object in enumerate(image_objects, start=1):
            label = f'{object["label"]}: {round(object["score"] * 100, 2)}%'
            color = (0, 0, 255)
            xmin, ymin, xmax, ymax = (
                30,
                60 * idx,
                60 * (idx + 1),
                30,
            )

            for img in imgs:
                cv2.putText(
                    img,
                    label,
                    (xmin, ymin - 15 if ymin - 15 > 15 else ymin + 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    color,
                    2,
                )

        return [
            av.VideoFrame.from_ndarray(img, format='bgr24')
            for img in imgs
        ]

    webrtc_streamer(
        key="sample",
        queued_video_frames_callback=queued_video_frames_callback,
        async_processing=True,
    )


def show_code_python() -> None:
    st.code(
        f'''
        # TODO: not supported yet
        ''',
        line_numbers=True,
    )


if __name__ == '__main__':
    st.title('Image :: Classification with Webcam Streaming')
    inputs = asyncio.run(get_inputs())
    code.show(globals(), inputs)
    asyncio.run(execute(**inputs))
