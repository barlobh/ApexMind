# Apexx IA Forensic Carver GUI (ApexMind)
# Upload a SHA1-named file from an iOS backup, view structured data or perform regex-based carving

import streamlit as st
import re
import sqlite3
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="ApexMind - Apexx IA Carver", layout="wide")
st.title("ApexMind - iOS Forensic File Carver")
st.markdown("""
Upload any SHA1-named file from an iOS backup.  
Choose to either **view structured content** (e.g., SQLite/PLIST)  
or **run deep carving** for phone numbers, emails, and deleted fragments.
""")

# Upload section
uploaded_file = st.file_uploader("📁 Upload SHA1-Named File", type=None)
manifest = st.file_uploader("🧾 (Optional) Upload Manifest.db", type=["db"])

if uploaded_file:
    file_bytes = uploaded_file.read()
    file_name = uploaded_file.name
    file_type = "Unknown"

    # Try to detect SQLite
    try:
        conn = sqlite3.connect(f"file:{file_name}?mode=ro", uri=True)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        file_type = "SQLite Database"
        conn.close()
    except Exception:
        if b"bplist" in file_bytes[:100]:
            file_type = "Binary PLIST"
        elif b"<!DOCTYPE html" in file_bytes[:100]:
            file_type = "HTML/Text"
        else:
            file_type = "Binary/Unknown"

    st.subheader(f"Detected File Type: {file_type}")

    mode = st.radio("Select Mode", ["View Structured Data", "Run Deep Carver"])

    if mode == "View Structured Data":
        if file_type == "SQLite Database":
            st.markdown("### SQLite Table Viewer")
            conn = sqlite3.connect(BytesIO(file_bytes))
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            selected_table = st.selectbox("Select Table to Preview", tables)
            cursor.execute(f"SELECT * FROM {selected_table} LIMIT 100")
            rows = cursor.fetchall()
            cols = [description[0] for description in cursor.description]
            df = pd.DataFrame(rows, columns=cols)
            st.dataframe(df)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Table as CSV", csv, f"{selected_table}.csv", "text/csv")
            conn.close()
        else:
            st.markdown("### File Preview")
            text = file_bytes.decode(errors="ignore")
            st.text_area("File Snippet:", text[:5000], height=300)

    elif mode == "Run Deep Carver":
        st.markdown("### Running Carving Engine...")
        patterns = {
            "Phone": r"(?<!\\d)(\\+?\\d{1,2})?[ -.]?(\\(?\\d{3}\\)?)[ -.]?\\d{3}[ -.]?\\d{4}(?!\\d)",
            "Email": r"[\\w\\.-]+@[\\w\\.-]+\\.[a-zA-Z]{2,}",
            "URL": r"https?://[\\w./-]+",
            "Timestamp": r"\\d{4}-\\d{2}-\\d{2}[ T]\\d{2}:\\d{2}(:\\d{2})?",
            "UTF-Text": r"[\\x20-\\x7E]{6,}"
        }

        decoded = file_bytes.decode(errors="ignore", errors="replace")
        results = []
        for label, pattern in patterns.items():
            for match in re.finditer(pattern, decoded):
                start = match.start()
                pre = decoded[max(0, start-20):start]
                post = decoded[match.end():match.end()+20]
                results.append({
                    "Type": label,
                    "Match": match.group(),
                    "Offset": start,
                    "PreContext": pre,
                    "PostContext": post
                })

        if results:
            df = pd.DataFrame(results)
            st.dataframe(df)
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("Download Carved Results", csv, "carved_results.csv", "text/csv")
        else:
            st.warning("No matches found with the current patterns.")
