# 🧠 ApexMind – Apexx IA iOS Forensic File Carver

### Description
A forensic carving tool built by Apexx IA to extract structured and unstructured data from iOS backup files.
Supports SHA1 file uploads, Manifest.db mapping, and regex-based deep carving.

### Usage
1. Upload any SHA1-named file (e.g. `3d0d7e5fb2ce288813306e4d4636395e047a3d28`).
2. Optional: Upload `Manifest.db` to resolve file paths and app sources.
3. Choose **View Structured Data** or **Run Deep Carver**.
4. Export results as CSV.

### Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
