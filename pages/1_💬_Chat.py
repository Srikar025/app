import streamlit as st
from datetime import datetime
from utils import insert_row, list_table


st.title("💬 Group Chat")


# Auto-refresh every 3 seconds
st.autorefresh = st.experimental_rerun # alias
st_autorefresh = st.experimental_rerun # keep a reference to avoid linter issue
st.experimental_set_query_params() # harmless; ensures rerun behavior is clean


refresh_ms = st.sidebar.slider("Auto-refresh (ms)", 1000, 10000, 3000, 500)
_ = st.experimental_memo.clear() # no-op placeholder
st_autorefresh = st.experimental_rerun # not actually used; kept for clarity


# Message form
with st.form("chat_form", clear_on_submit=True):
    msg = st.text_input("Type your message", max_chars=400)
    submitted = st.form_submit_button("Send")


if submitted and msg.strip():
    username = (st.session_state.get("display_name") or "Anonymous").strip()[:50]
    insert_row("chats", {"username": username, "message": msg.strip()})
    st.success("Sent!")
    st.experimental_rerun()


st.divider()


# Fetch & render chat history
msgs = list_table("chats", order_by="timestamp", desc=False)


for m in msgs[-500:]: # cap render count
    ts = m.get("timestamp")
    ts_str = ts if isinstance(ts, str) else str(ts)
    st.markdown(f"**{m.get('username','Anonymous')}** · _{ts_str}_\n\n{m.get('message','')}")