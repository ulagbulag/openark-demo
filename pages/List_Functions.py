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

    # 3. Query all functions that you can use
    function_names = ark.list_functions()

    # 4. Show outputs
    st.table({
        'Function Name': function_names,
    })


def show_code_python() -> None:
    st.code(
        f'''
        # 1. Import needed libraries
        from openark import OpenArk
        
        # 2. Create an OpenARK instance
        ark = OpenArk()
        
        # 3. Query all functions that you can use
        function_names = ark.list_functions()
        
        # 4. Show outputs
        print(function_names)
        ''',
        line_numbers=True,
    )


if __name__ == '__main__':
    st.title('List Functions')
    inputs = asyncio.run(get_inputs())
    code.show(globals(), inputs)
    asyncio.run(execute(**inputs))
