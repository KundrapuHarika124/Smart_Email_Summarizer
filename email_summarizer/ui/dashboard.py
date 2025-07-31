# dashboard.py
import streamlit as st
import os

def show_dashboard(emails):
    st.title("📥 Inbox Summary")

    if st.button("🚪 Logout"):
        st.session_state.clear()
        if os.path.exists("auth/token.pickle"):
            os.remove("auth/token.pickle")
        st.rerun()


    for email in emails:
        with st.expander(f"📨 {email['subject']}"):
            st.markdown(f"**From:** {email['sender']}")
            st.markdown(f"**Date:** {email['date']}")
            st.markdown(f"**Message:**\n\n{email['snippet']}")
            if email['attachments']:
                st.markdown("📎 **Attachments:**")
                for file in email['attachments']:
                    st.markdown(f"• {file}")
