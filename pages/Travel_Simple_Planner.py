import asyncio
from typing import Any

import streamlit as st

from utils import code


async def get_inputs() -> dict[str, Any]:
    return {
        # NOTE: Ordered UI
        'language': st.selectbox(
            label='Output Language',
            options=[
                'English',
                'Korean',
            ],
        ),
        'departure': st.text_input(
            label='Departure',
            value='Gwangju',
        ),
        'destinations': st.text_input(
            label='Destinations',
            value='Paris',
        ),
        'activities': st.multiselect(
            label='Activities',
            options=[
                'Drinking',
                'Famous Cuisine',
                'Famous Restaurant',
                'Historic Sites',
            ],
            default=[
                'Famous Restaurant',
                'Historic Sites',
            ],
        ),
        'level': st.selectbox(
            label='Activity Level',
            options=[
                'Normal',
                'Spacious',
                'Tight',
            ],
        ),
        'nights': st.slider(
            label='Number of Nights',
            min_value=0,
            max_value=30,
            value=4,
        ),
        'days': st.slider(
            label='Number of Days',
            min_value=1,
            max_value=31,
            value=5,
        ),
    }


async def execute(
    language: str,
    departure: str,
    destinations: str,
    activities: list[str],
    level: str,
    nights: int,
    days: int,
) -> None:
    # 1. Import needed libraries
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.prompts import ChatPromptTemplate

    # 2. Import a selected LLM model
    from langchain_openai import ChatOpenAI

    # 3. Create a prompt template
    prompt = ChatPromptTemplate.from_messages([
        ('system', f'Hello, I am a travel planner. Where do you want to go?'),
        ('user', f'{destinations}.'),
        ('system', f'Where do you want to depart from?'),
        ('user', f'{departure}.'),
        ('system', f'How long do you want to go travel?'),
        ('user', f'{days} days {nights} nights.'),
        ('system', f'Which activities do you want to do?'),
        ('user', f'{", ".join(activities)}.'),
        ('system', f'How detailed should my travel plan be?'),
        ('user', f'{level}.'),
        ('system', f'All right. Let me create the best per-hour travel plan based on the information you provide, including the start and end times for each plan. After answering, I will help you make reservations.'),
        ('user',
         f'Ok. Please answer in standard {language}. Don\'t ask me any more questions, but answer using the information you have.'),
    ])
    chain = prompt

    # 4. Connect a LLM model
    llm = ChatOpenAI(
        model='gpt-4-turbo-preview',
    )
    chain |= llm

    # 5. Attach an output parser
    output_parser = StrOutputParser()
    chain |= output_parser

    # 6. Execute the LLM chain with given context
    with st.spinner('Running LLM chain...'):
        response = chain.invoke({})

    # 7. Show outputs
    st.write(response)


def show_code_python(**_) -> None:
    st.code(
        f'''
        # NOTE: not implemented
        ''',
        line_numbers=True,
    )


if __name__ == '__main__':
    st.title('Travel :: Simple Planner')
    inputs = asyncio.run(get_inputs())
    code.show(globals(), inputs)
    asyncio.run(execute(**inputs))
