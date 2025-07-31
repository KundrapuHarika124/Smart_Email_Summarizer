# login.py
import streamlit as st

def show_login_button(auth_url):
    st.set_page_config(page_title="Smart Email Summarizer", layout="centered")
    st.title("📬 Smart Email Summarizer")
    st.markdown("Please log in with your Google account to begin.")

    st.markdown("### 🔐 Please sign in with your Google account to continue")
    st.markdown(f"[**👉 Continue with Google**]({auth_url})", unsafe_allow_html=True)
