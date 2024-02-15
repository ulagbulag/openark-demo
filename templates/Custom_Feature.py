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

    # TODO(user): write your code here!
    # 3. Do your works...
    ...


def show_code_python() -> None:
    st.code(
        f'''
        # 1. Import needed libraries
        from openark import OpenArk
        
        # 2. Create an OpenARK instance
        ark = OpenArk()
        
        # TODO(user): write your code here!
        # 3. Do your works...
        ...
        ''',
        line_numbers=True,
    )


if __name__ == '__main__':
    st.title('My Custom Feature')  # TODO(user): edit the feature title!
    inputs = asyncio.run(get_inputs())
    code.show(globals(), inputs)
    asyncio.run(execute(**inputs))
