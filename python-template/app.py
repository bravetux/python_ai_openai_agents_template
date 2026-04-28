"""Streamlit chat UI."""

import streamlit as st

from {{ project_slug_underscore }}.agents.orchestrator import build_orchestrator
from {{ project_slug_underscore }}.ui.components import render_chat_history, settings_sidebar


def main() -> None:
    st.set_page_config(page_title="{{ project_slug }}", page_icon="🤖", layout="wide")
    st.title("{{ project_slug }}")

    settings_sidebar()

    if "history" not in st.session_state:
        st.session_state.history = []
    if "orchestrator" not in st.session_state:
        st.session_state.orchestrator = build_orchestrator()

    render_chat_history(st.session_state.history)

    if prompt := st.chat_input("Ask the agent…"):
        st.session_state.history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking…"):
                answer = str(st.session_state.orchestrator(prompt))
                st.markdown(answer)

        st.session_state.history.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
