import streamlit as st


def init_state():
    if "message" not in st.session_state:
        st.session_state.message = []


def add_message(role: str, content: str, dataframe=None):
    msg = {"role": role, "content": content}
    if dataframe is not None:
        msg["dataframe"] = dataframe
    st.session_state.message.append(msg)
