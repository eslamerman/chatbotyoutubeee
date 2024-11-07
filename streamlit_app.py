# streamlit_app.py
import streamlit as st
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from urllib.parse import urlparse

# Config and Error Handling
def get_config():
  try:
    return {
      "web": {
        "client_id": st.secrets["GOOGLE_CLIENT_ID"],
        "client_secret": st.secrets["GOOGLE_CLIENT_SECRET"],
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [st.secrets.get("DEPLOYMENT_URL", "http://localhost:8501")],
        "javascript_origins": [st.secrets.get("DEPLOYMENT_URL", "http://localhost:8501")]
      }
    }
  except KeyError:
    st.error("""
      Missing required secrets. Please add the following to your secrets:
      - GOOGLE_CLIENT_ID
      - GOOGLE_CLIENT_SECRET
      - DEPLOYMENT_URL
  
      Go to your Streamlit app settings -> Secrets and add them in TOML format:
      ```toml
      GOOGLE_CLIENT_ID = "your-google-client-id"
      GOOGLE_CLIENT_SECRET = "your-google-client-secret"
      DEPLOYMENT_URL = "[https://chatbotyoutubeee.streamlit.app](https://chatbotyoutubeee.streamlit.app)"
      ```
    """)
    st.stop()

# Google Authentication Class
class GoogleAuth:
  def __init__(self, client_config):
    self.client_config = client_config
    self.flow = None

  def get_redirect_uri(self):
    if st.session_state.get('current_url'):
      parsed_url = urlparse(st.session_state.current_url)
      base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
      return base_url
    return self.client_config['web']['redirect_uris'][0]

  def initialize_flow(self):
    self.flow = Flow.from_client_config(
      self.client_config,
      scopes=['https://www.googleapis.com/auth/userinfo.profile',
              'https://www.googleapis.com/auth/userinfo.email'],
      redirect_uri=self.get_redirect_uri()
    )

  def get_authorization_url(self):
    if not self.flow:
      self.initialize_flow()
    auth_url, _ = self.flow.authorization_url(
      access_type='offline',
      include_granted_scopes='true',
      prompt='consent'
    )
    return auth_url

  def get_user_info(self, code):
    if not self.flow:
      self.initialize_flow()
    self.flow.fetch_token(code=code)
    credentials = self.flow.credentials

    service = build('oauth2', 'v2', credentials=credentials)
    user_info = service.userinfo().get().execute()
    return user_info

# Session State Initialization
def initialize_session_state():
  if 'user_info' not in st.session_state:
    st.session_state.user_info = None
  if 'authentication_error' not in st.session_state:
    st.session_state.authentication_error = None
  st.session_state.current_url = st.secrets.get("DEPLOYMENT_URL", "http://localhost:8501")

# Main Application
def main():
  st.set_page_config(
    page_title="YouTube Chatbot Login",
    page_icon="",
    initial_sidebar_state="expanded"
  )

  # Initialize session state
  initialize_session_state()

  # Create two columns for the header
  col1, col2 = st.columns([3, 1])
  with col1:
    st.title(" YouTube Chatbot")

  # Show any authentication errors
  if st.session_state.authentication_error:
