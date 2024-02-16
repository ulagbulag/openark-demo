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

    # 3. Load global namespace
    with st.spinner('Loading Global Namespace...'):
        gn = ark.get_global_namespace()

    # 4. Define the UWB Location Dataset name
    model_name = 'footprint'

    # 5. Query 10 latest rows
    lf = gn.sql(
        f'SELECT * FROM {model_name} ORDER BY __timestamp DESC LIMIT 10')

    # 6. Collect data (Execute)
    df = lf.collect()

    # 7. Show outputs
    st.table(df)


def show_code_python() -> None:
    st.code(
        f'''
        # 1. Import needed libraries
        from openark import OpenArk

        # 2. Create an OpenARK instance
        ark = OpenArk()

        # 3. Load global namespace
        gn = ark.get_global_namespace()

        # 4. Define the UWB Location Dataset name
        model_name = 'footprint'

        # 5. Query 10 latest rows
        lf = gn.sql(
            f'SELECT * FROM {{model_name}} ORDER BY __timestamp DESC LIMIT 10')

        # 6. Collect data (Execute)
        df = lf.collect()

        # 7. Show outputs
        print(df)

        ''',
        line_numbers=True,
    )


if __name__ == '__main__':
    st.title('UWB :: Query with SQL')
    inputs = asyncio.run(get_inputs())
    code.show(globals(), inputs)
    asyncio.run(execute(**inputs))
