import os
import streamlit as st

st.set_page_config(page_title="Chat + giscus comments", page_icon="💬", layout="centered")

# ---------- App header
st.title("💬 Streamlit Chat + giscus Comments")
st.caption("Simple local chat interface with an embedded giscus discussion thread for feedback.")

# ---------- Demo chat state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Ask me anything, and leave feedback below in the giscus section."}
    ]

# ---------- Chat UI
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if user_text := st.chat_input("Type a message and press Enter"):
    st.session_state.messages.append({"role": "user", "content": user_text})
    # --- Dummy bot reply (replace with your LLM call if desired)
    bot_reply = f"You said: {user_text}"
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})
    st.rerun()

# ---------- Controls
with st.sidebar:
    st.header("Settings")
    if st.button("Clear chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat cleared. Start a new conversation!"}
        ]
        st.rerun()

    st.subheader("giscus mapping")
    mapping_choice = st.selectbox(
        "How should giscus map this page to a discussion?",
        options=["specific", "url", "pathname", "title"],
        index=0,
        help=(
            "'specific' lets you name the thread. 'url' uses the full page URL.\n"
            "'pathname' uses just the path. 'title' uses the page title."
        ),
    )

    default_term = "Streamlit Chat App"
    if mapping_choice == "specific":
        term = st.text_input("Thread name (data-term)", value=default_term)
    elif mapping_choice == "title":
        term = st.text_input("Title to match (data-term)", value=st.get_option("server.headless") and "Streamlit" or st.title)
    else:
        term = ""  # not used by url/pathname

# ---------- giscus configuration (replace with your values)
# Prefer storing these in .streamlit/secrets.toml
# [giscus]
# repo = "OWNER/REPO"
# repo_id = "R_kgDO..."
# category = "General"
# category_id = "DIC_kwDO..."

REPO = st.secrets.get("giscus", {}).get("repo", os.getenv("GISCUS_REPO", "OWNER/REPO"))
REPO_ID = st.secrets.get("giscus", {}).get("repo_id", os.getenv("GISCUS_REPO_ID", "R_kgDO_REPOID"))
CATEGORY = st.secrets.get("giscus", {}).get("category", os.getenv("GISCUS_CATEGORY", "General"))
CATEGORY_ID = st.secrets.get("giscus", {}).get("category_id", os.getenv("GISCUS_CATEGORY_ID", "DIC_kwDO_CATEGORYID"))
LANG = st.secrets.get("giscus", {}).get("lang", os.getenv("GISCUS_LANG", "en"))
THEME = st.secrets.get("giscus", {}).get("theme", os.getenv("GISCUS_THEME", "preferred_color_scheme"))

# ---------- Embed giscus via a small HTML snippet
from textwrap import dedent

def render_giscus(repo: str, repo_id: str, category: str, category_id: str, mapping: str, term: str, lang: str, theme: str):
    # Validate minimal config
    missing = [
        k for k, v in {
            "data-repo": repo,
            "data-repo-id": repo_id,
            "data-category": category,
            "data-category-id": category_id,
        }.items() if not v or v.startswith("OWNER/") or v.endswith("_ID")
    ]
    if missing:
        st.warning(
            "giscus is not configured yet. Open the sidebar and set your repository IDs in secrets."
        )

    html = f"""
        <script src="https://giscus.app/client.js"
            data-repo="{repo}"
            data-repo-id="{repo_id}"
            data-category="{category}"
            data-category-id="{category_id}"
            data-mapping="{mapping}"
            {f'data-term="{term}"' if mapping == 'specific' or mapping == 'title' else ''}
            data-strict="0"
            data-reactions-enabled="1"
            data-emit-metadata="0"
            data-input-position="bottom"
            data-theme="{theme}"
            data-lang="{lang}"
            crossorigin="anonymous"
            async>
        </script>
        <noscript>Enable JavaScript to view the <a href="https://giscus.app">giscus</a> comments.</noscript>
    """
    st.components.v1.html(dedent(html), height=540, scrolling=True)

st.divider()
st.subheader("💬 Comments & feedback")
render_giscus(
    repo=REPO,
    repo_id=REPO_ID,
    category=CATEGORY,
    category_id=CATEGORY_ID,
    mapping=mapping_choice,
    term=term,
    lang=LANG,
    theme=THEME,
)

st.caption(
    "giscus uses GitHub Discussions for storage. To comment, sign in with your GitHub account in the widget above."
)
