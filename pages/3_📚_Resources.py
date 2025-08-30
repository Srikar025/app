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
        desc = st.text_area("Description")
        file = st.file_uploader("Upload file", type=None)
        submitted = st.form_submit_button("Upload Resource")
    
    if submitted and title:
        file_url = ""
        if file is not None:
            file_url = upload_to_bucket(st.secrets["BUCKET_RESOURCES"], file, subdir="resources")
        insert_row("resources", {
            "title": title.strip()[:120],
            "description": (desc or "").strip(),
            "file_url": file_url
        })
        st.success("Resource uploaded!")
        st.experimental_rerun()


st.divider()


st.subheader("All Resources")
items = list_table("resources", order_by="uploaded_at", desc=True)

if not items:
    st.info("No resources yet.")
else:
    for r in items:
        st.markdown(f"### {r['title']}")
        if r.get("description"):
            st.write(r["description"])
        if r.get("file_url"):
            st.write(f"[Download / View]({r['file_url']})")
        st.markdown("---")