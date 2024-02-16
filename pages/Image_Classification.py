import asyncio
from typing import Any

import streamlit as st

from utils import code, upload


async def get_inputs() -> dict[str, Any]:
    return {
        'image': upload.any_image(),
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

    # 3. Define the Image Classification function
    function_name = 'image-classification'

    # 4. Load the function
    with st.spinner('Loading a function...'):
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

    # 9. Show outputs
    st.table(image_objects)


def show_code_python(image: Any | None) -> None:
    # 0. Check inputs
    if image is not None:
        image_name: str = image.name
    else:
        return

    st.code(
        f'''
        # 0. Check inputs
        image_name = {image_name!r}
        image_data = open(image_name, 'rb').read()


        # 1. Import needed libraries
        from openark import OpenArk

        # 2. Create an OpenARK instance
        ark = OpenArk()

        # 3. Define the Image Classification function
        function_name = 'image-classification'

        # 4. Load the function
        function = await ark.get_function(function_name)

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

        # 7. Call the function and return the output message
        input_message = await function(
            value=input_value,
            payloads=input_payloads,
        )

        # 8. Find the results
        image_objects = input_message['value']

        # 9. Show outputs
        print(image_objects)

        ''',
        line_numbers=True,
    )


if __name__ == '__main__':
    st.title('Image :: Classification')
    inputs = asyncio.run(get_inputs())
    code.show(globals(), inputs)
    asyncio.run(execute(**inputs))
