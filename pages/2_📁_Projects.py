import streamlit as st
from utils import upload_to_bucket, insert_row, list_table


st.title("📁 Projects Showcase")


with st.form("proj_form"):
    name = st.text_input("Your Name", value=st.session_state.get("display_name", ""))
    title = st.text_input("Project Title")
    desc = st.text_area("Short Description")
    file = st.file_uploader("Optional: Attach a file (zip/pdf/pptx/png/jpg)", type=None)
    submitted = st.form_submit_button("Upload Project")


if submitted:
    if not name or not title:
        st.error("Name and Title are required.")
    else:
        file_url = ""
        if file is not None:
            file_url = upload_to_bucket(st.secrets["BUCKET_PROJECTS"], file, subdir="projects")
        insert_row("projects", {
            "name": name.strip()[:80],
            "title": title.strip()[:120],
            "description": (desc or "").strip(),
            "file_url": file_url
        })
        st.success("Project uploaded!")
        st.rerun()


st.divider()


st.subheader("All Projects")
items = list_table("projects", order_by="uploaded_at", desc=True)


if not items:
    st.info("No projects yet. Be the first to upload!")
else:
    for p in items:
        st.markdown(f"### {p['title']}")
        st.markdown(f"**By:** {p['name']}")
        if p.get("description"):
            st.write(p["description"])
        if p.get("file_url"):
            st.write(f"[Download / View]({p['file_url']})")
        st.markdown("---")