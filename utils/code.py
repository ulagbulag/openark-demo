from typing import Any

import streamlit as st


def show(globals: dict[str, Any], variables: dict[str, Any] | None = None) -> None:
    variables = variables or {}

    with st.expander('Code'):
        fn_name_prefix = 'show_code_'
        tab_names = {
            name: name[len(fn_name_prefix):].title()
            for name in globals
            if name.startswith(fn_name_prefix)
        }
        tabs = st.tabs(tab_names.values())
        for name, tab in zip(tab_names, tabs):
            with tab:
                globals[name](**variables)
