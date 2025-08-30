import streamlit as st


st.set_page_config(page_title="Student Community", page_icon="🎓", layout="centered")


st.title("🎓 Student Community Portal")
st.markdown(
"""
Welcome! Use the sidebar to navigate:
- **💬 Chat**: group chat in real time (auto-refresh)
- **📁 Projects**: upload and showcase student projects
- **📚 Resources**: browse resources; upload is password-gated


> This app is intentionally simple: no login. Please be respectful.
"""
)


# Simple display name stored in session (used by Chat/Projects)
with st.sidebar:
    st.header("Your Display Name")
    st.text_input("Name", key="display_name", placeholder="e.g., Priya")
    st.caption("Used for chat & project uploads. Optional.")


st.info("Tip: Set your name in the sidebar before chatting or uploading projects.")
