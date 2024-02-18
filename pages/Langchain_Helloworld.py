import asyncio
from typing import Any

import streamlit as st

from utils import code


async def get_inputs() -> dict[str, Any]:
    return {
        # NOTE: Ordered UI
        'type': st.selectbox(
            label='LLM Model',
            help='Please choose which LLM engine do you want to use.',
            options=[
                'OpenAI',
            ],
        ),
        'context': st.text_input(
            label='Context (prompt)',
            value='Please plan a 6 nights and 7 days trip in Paris, France.',
            help='Please write your prompt context.',
        )
    }


async def execute(type: str, context: str) -> None:
    # 1. Import needed libraries
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate

    # 2. Import a selected LLM model
    ChatModel = getattr(
        __import__(
            name=f'langchain_{type.lower()}',
            fromlist=(f'Chat{type}'),
        ),
        f'Chat{type}',
    )

    # 3. Create a prompt template
    prompt = ChatPromptTemplate.from_messages([
        ('user', '{input_context}'),
    ])
    chain = prompt

    # 4. Connect a LLM model
    llm = ChatModel()
    chain |= llm

    # 5. Attach an output parser
    output_parser = StrOutputParser()
    chain |= output_parser

    # 6. Execute the LLM chain with given context
    with st.spinner('Running LLM chain...'):
        response = chain.invoke({
            'input_context': context,
        })

    # 7. Show outputs
    st.write(response)


def show_code_python(type: str, context: str) -> None:
    st.code(
        f'''
        # 1. Import needed libraries
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import ChatPromptTemplate

        # 2. Import a selected LLM model
        from langchain_{type.lower()} import Chat{type}

        # 3. Create a prompt template
        prompt = ChatPromptTemplate.from_messages([
            ('user', '{{input_context}}'),
        ])
        chain = prompt

        # 4. Connect a LLM model
        llm = Chat{type}()
        chain |= llm

        # 5. Attach an output parser
        output_parser = StrOutputParser()
        chain |= output_parser

        # 6. Execute the LLM chain with given context
        response = chain.invoke({{
            'input_context': {context!r},
        }})

        # 7. Show outputs
        print(response)

        ''',
        line_numbers=True,
    )


if __name__ == '__main__':
    st.title('Langchain :: Hello World!')
    inputs = asyncio.run(get_inputs())
    code.show(globals(), inputs)
    asyncio.run(execute(**inputs))
