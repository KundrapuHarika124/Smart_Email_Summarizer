import os
import pickle
import streamlit as st
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

CLIENT_SECRET_FILE = "auth/credentials.json"
TOKEN_FILE = "auth/token.pickle"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def login():
    creds = None

    # ✅ 1. Load token if available
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)
        if creds and creds.valid:
            return creds
        elif creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_FILE, "wb") as token:
                pickle.dump(creds, token)
            return creds

    # ✅ 2. Handle ?code= from redirect
    query_params = st.query_params
    if "code" in query_params:
        if "flow" not in st.session_state:
            st.error("❌ Missing OAuth flow. Please restart login.")
            return None

        try:
            flow = st.session_state.flow
            flow.fetch_token(code=query_params["code"][0])
            creds = flow.credentials

            with open(TOKEN_FILE, "wb") as token:
                pickle.dump(creds, token)

            st.success("✅ Login successful! Reloading...")
            st.experimental_rerun()
            return None
        except Exception as e:
            st.error(f"❌ Login failed: {str(e)}")
            return None

    # ✅ 3. Not logged in yet — generate login link and store flow
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri="http://localhost:8501"
    )
    auth_url, _ = flow.authorization_url(prompt='consent')

    st.session_state.flow = flow  # ✅ Save it for post-redirect token exchange
    st.markdown(f"[🔐 Click here to log in with Google]({auth_url})")

    return None


def get_gmail_service(creds):
    return build("gmail", "v1", credentials=creds)
