import os
import pickle
import streamlit as st

from auth.google_auth import login, get_gmail_service
from gmail.fetch_emails import fetch_emails
from ui.dashboard import show_dashboard

st.set_page_config(page_title="Smart Email Summarizer", layout="wide")
st.title("📨 Smart Email Summarizer")

creds = login()

if creds:
    service = get_gmail_service(creds)
    emails = fetch_emails(service)
        # Show logout button
    if st.sidebar.button("🚪 Logout"):
        if os.path.exists("auth/token.pickle"):
            os.remove("auth/token.pickle")
            st.success("✅ Logged out!")
            st.experimental_rerun()

    # Show dashboard UI
    show_dashboard(emails)

else:
    st.info("🔐 Please log in to access your inbox.")