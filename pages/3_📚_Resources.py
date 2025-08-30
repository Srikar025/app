import streamlit as st
from utils import upload_to_bucket, insert_row, list_table


st.title("📚 Resources")


# Gate the upload form behind a simple password
if "resources_ok" not in st.session_state:
st.session_state["resources_ok"] = False


if not st.session_state["resources_ok"]:
with st.form("pw_form"):
pw = st.text_input("Enter upload password", type="password")
ok = st.form_submit_button("Unlock Upload")
if ok:
if pw == st.secrets["RESOURCES_PASSWORD"]:
st.session_state["resources_ok"] = True
st.success("Upload unlocked.")
st.experimental_rerun()
else:
st.error("Incorrect password.")


if st.session_state["resources_ok"]:
st.subheader("Upload a Resource")
with st.form("res_form"):
title = st.text_input("Title")
desc