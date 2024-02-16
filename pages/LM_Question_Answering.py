import asyncio
from typing import Any

import streamlit as st

from utils import code


async def get_inputs() -> dict[str, Any]:
    return {
        'context': st.text_input(
            label='Context',
            value='Hello, my name is Ho Kim and I love NetAI!',
        ),
        'question': st.text_input(
            label='Question',
            value='What is my name?',
        ),
    }


async def execute(context: str, question: str) -> None:
    with st.spinner('Initializing OpenARK...'):
        # 1. Import needed libraries
        from openark import OpenArk

        # 2. Create an OpenARK instance
        ark = OpenArk.cloned()

    # 3. Define the Question Answering function
    function_name = 'question-answering'

    # 4. Load the function
    with st.spinner('Loading a function...'):
        function = await ark.get_function(function_name)

    # 5. Make an input value
    input_value = {
        'context': context,
        'question': question,
    }

    # 6. Call the function and return the output message
    output_message = await function(input_value)

    # 7. Show outputs
    st.write({
        'answer': output_message['answer'],
        'score': output_message['score'],
    })


def show_code_python(context: str, question: str) -> None:
    st.code(
        f'''
        # 1. Import needed libraries
        from openark import OpenArk

        # 2. Create an OpenARK instance
        ark = OpenArk()

        # 3. Define the Question Answering function
        function_name = 'question-answering'

        # 4. Load the function
        function = await ark.get_function(function_name)

        # 5. Make an input value
        input_value = {{
            'context': {context!r},
            'question': {question!r},
        }}

        # 6. Call the function and return the output message
        output_message = await function(input_value)

        # 7. Show outputs
        print({{
            'answer': output_message['answer'],
            'score': output_message['score'],
        }})

        ''',
        line_numbers=True,
    )


if __name__ == '__main__':
    st.title('LM :: Question Answering')
    inputs = asyncio.run(get_inputs())
    code.show(globals(), inputs)
    asyncio.run(execute(**inputs))
