import os

# Path to the anonymized Slack data (not tracked by git)
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "anonymized")

# MongoDB Atlas — check Streamlit secrets first, then environment variable
try:
    import streamlit as st
    MONGO_URI = st.secrets.get("MONGO_URI", os.environ.get("MONGO_URI", ""))
except Exception:
    MONGO_URI = os.environ.get("MONGO_URI", "")

MONGO_DB = "gebeya_slack"
