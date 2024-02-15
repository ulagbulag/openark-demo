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

    # 3. Define the UWB Location Dataset name
    model_name = 'footprint'

    # 4. Open a model channel
    with st.spinner('Opening model channel...'):
        model = await ark.get_model_channel(model_name)
        if model._subscriber._inner is not None:
            model._subscriber._inner._send_unsubscribe()

    # 5. Start subscribing
    with st.spinner('Subscribing...'):
        with st.empty():
            table = []
            st.table(table)

            async for data in model:

                # 6. Show outputs
                table.append(data)
                st.table(table)

                if len(table) > 12:
                    del table[0]


def show_code_python() -> None:
    st.code(
        f'''
        # 1. Import needed libraries
        from openark import OpenArk
        
        # 2. Create an OpenARK instance
        ark = OpenArk()
        
        # 3. Define the UWB Location Dataset name
        model_name = 'footprint'
        
        # 4. Open a model channel
        model = await ark.get_model_channel(model_name)

        # 5. Start subscribing
        async for data in model:

            # 6. Show outputs
            print(data)
        ''',
        line_numbers=True,
    )


if __name__ == '__main__':
    st.title('Subscribe Models (Topics)')
    inputs = asyncio.run(get_inputs())
    code.show(globals(), inputs)
    asyncio.run(execute(**inputs))
