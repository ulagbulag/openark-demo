import streamlit as st


def main():
    st.title('Welcome to OpenARK Demo!')

    with st.spinner('Initializing OpenARK...'):
        from openark import OpenArk
        _ = OpenArk(register_global=True)


if __name__ == '__main__':
    main()
