from uuid import uuid4
from datetime import date
from pathlib import Path
import mimetypes
import re
import streamlit as st
from supabase_client import get_client


SAFE_CHARS = re.compile(r"[^a-zA-Z0-9_.-]")


def sanitize_filename(name: str) -> str:
    return SAFE_CHARS.sub("_", name)


@st.cache_data(show_spinner=False)
def list_table(table: str, order_by: str, desc: bool = True):
    supabase = get_client()
    q = supabase.table(table).select("*").order(order_by, desc=desc)
    res = q.execute()
    return res.data or []




def insert_row(table: str, payload: dict):
    try:
        supabase = get_client()
        return supabase.table(table).insert(payload).execute()
    except Exception as e:
        st.error(f"Database operation failed: {str(e)}")
        raise e




def upload_to_bucket(bucket: str, file, subdir: str = "") -> str:
    """Upload a Streamlit UploadedFile to Supabase Storage and return public URL."""
    if not file:
        return ""
    
    try:
        supabase = get_client()
        bucket_client = supabase.storage.from_(bucket)

        original = sanitize_filename(file.name)
        ext = Path(original).suffix
        key = f"{subdir}/{date.today().isoformat()}/{uuid4().hex}{ext}" if subdir else f"{date.today().isoformat()}/{uuid4().hex}{ext}"

        content_type = mimetypes.guess_type(original)[0] or "application/octet-stream"
        data = file.getvalue() # bytes

        # Upload
        bucket_client.upload(key, data, {"content-type": content_type})

        # Public URL (bucket must be public or have read policy)
        public_url = bucket_client.get_public_url(key)
        return public_url
    except Exception as e:
        st.error(f"File upload failed: {str(e)}")
        return ""