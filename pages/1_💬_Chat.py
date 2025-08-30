import streamlit as st
from datetime import datetime
from utils import insert_row, list_table


st.title("💬 Group Chat")


# Auto-refresh settings
refresh_ms = st.sidebar.slider("Auto-refresh (ms)", 1000, 10000, 3000, 500)
st.sidebar.info(f"Page will refresh every {refresh_ms//1000} seconds")


# Message form
with st.form("chat_form", clear_on_submit=True):
    msg = st.text_input("Type your message", max_chars=400)
    submitted = st.form_submit_button("Send")


if submitted and msg.strip():
    try:
        username = (st.session_state.get("display_name") or "Anonymous").strip()[:50]
        insert_row("chats", {"username": username, "message": msg.strip()})
        st.success("Message sent!")
        st.rerun()
    except Exception as e:
        st.error(f"Failed to send message: {str(e)}")


st.divider()

# Manual refresh button
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🔄 Refresh"):
        st.rerun()
with col2:
    st.write("Click to manually refresh messages")

st.divider()

# Fetch & render chat history
try:
    msgs = list_table("chats", order_by="timestamp", desc=False)
    
    if not msgs:
        st.info("No messages yet. Be the first to send a message!")
    else:
        st.subheader(f"Chat History ({len(msgs)} messages)")
        
        # Display messages in a container for better scrolling
        chat_container = st.container()
        with chat_container:
            for m in msgs[-500:]: # cap render count
                ts = m.get("timestamp")
                ts_str = ts if isinstance(ts, str) else str(ts)
                
                # Create a message card
                with st.expander(f"💬 {m.get('username','Anonymous')} · {ts_str}", expanded=True):
                    st.write(m.get('message',''))
                    st.caption(f"Sent at: {ts_str}")
                
except Exception as e:
    st.error(f"Error loading messages: {str(e)}")
    st.info("Please check your database connection.")