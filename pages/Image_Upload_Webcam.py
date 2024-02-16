import asyncio
from typing import Any

import streamlit as st

from utils import code, upload


async def get_inputs() -> dict[str, Any]:
    return {
        'image': upload.webcam(),
    }


async def execute(image: Any | None) -> None:
    # 0. Check inputs
    if image is not None:
        image_name: str = image.name
        image_data: bytes = image.getvalue()
    else:
        return

    with st.spinner('Initializing OpenARK...'):
        # 1. Import needed libraries
        from openark import OpenArk

        # 2. Create an OpenARK instance
        ark = OpenArk.cloned()

    # 3. Define the image model
    model_name = 'image'

    # 4. Open a model channel
    with st.spinner('Opening model channel...'):
        model = await ark.get_model_channel(model_name)

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

    # 7. Upload the data and return the input message
    input_message = await model.publish(
        value=input_value,
        payloads=input_payloads,
    )

    # 8. Find the sent input payload image
    image_payload = input_message['__payloads'][0]

    # 9. Show outputs
    st.write({
        'URL': model.get_payload_url(image_payload),
        'size': len(image_data),
    })


def show_code_python(image: Any | None) -> None:
    # 0. Check inputs
    if image is not None:
        image_name: str = image.name
    else:
        return

    st.code(
        f'''
        # 0. Check inputs
        def capture_image(save_path: str) -> bytes:
            import cv2

            cap = cv2.VideoCapture(0)  # on Linux, /dev/video0 should be exists
            ret, frame = cap.read()
            if not ret:
                raise Exception('Failed to capture an image from the given webcam')

            cv2.imwrite(save_path, frame)
            return open(save_path, 'rb').read()

        image_name = 'webcam_image.jpg'
        image_data = capture_image(image_name)


        # 1. Import needed libraries
        from openark import OpenArk

        # 2. Create an OpenARK instance
        ark = OpenArk()

        # 3. Define the image model
        model_name = 'image'

        # 4. Open a model channel
        model = await ark.get_model_channel(model_name)

        # 5. Make input payloads
        input_payloads = {{
            image_name: image_data,
        }}

        # 6. Make an input value
        input_value = {{
            # NOTE: the prefix "@data:image" describes that this payload data is an image.
            'images': [
                f'@data:image,{{image_name}}',
            ],
        }}

        # 7. Upload the data and return the input message
        input_message = await model.publish(
            value=input_value,
            payloads=input_payloads,
        )

        # 8. Find the sent input payload image
        image_payload = input_message['__payloads'][0]

        # 9. Show outputs
        print({{
            'URL': model.get_payload_url(image_payload),
            'size': len(image_data),
        }})

        ''',
        line_numbers=True,
    )


if __name__ == '__main__':
    st.title('Image :: Upload Webcam')
    inputs = asyncio.run(get_inputs())
    code.show(globals(), inputs)
    asyncio.run(execute(**inputs))
