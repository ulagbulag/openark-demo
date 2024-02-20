import asyncio
from typing import Any

import streamlit as st

from utils import code


async def get_inputs() -> dict[str, Any]:
    return {}


async def execute() -> None:
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

    # 5. Start subscribing
    with st.spinner('Subscribing (~10 fps)...'):
        with st.empty():
            async for data in model:

                # 6. Parse image data
                image = bytes(data['__payloads'][0]['value'])

                # 7. Show outputs
                st.image(image)
                await asyncio.sleep(0.1)


def show_code_python() -> None:
    st.code(
        f'''
        # 1. Import needed libraries
        from openark import OpenArk

        # 2. Create an OpenARK instance
        ark = OpenArk()

        # 3. Define the UWB Location Dataset name
        model_name = 'image'

        # 4. Open a model channel
        model = await ark.get_model_channel(model_name)

        # 5. Start subscribing
        async for data in model:

            # 6. Parse image data
            image = bytes(data['__payloads'][0]['value'])

            # 7. Show outputs
            print(data)

        ''',
        line_numbers=True,
    )


if __name__ == '__main__':
    st.title('Image :: Real-time Subscribing')
    inputs = asyncio.run(get_inputs())
    code.show(globals(), inputs)
    asyncio.run(execute(**inputs))
