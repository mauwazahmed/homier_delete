import streamlit as st
import requests
from authlib.integrations.requests_client import OAuth2Session

# Google OAuth Config
CLIENT_ID = "YOUR_GOOGLE_CLIENT_ID"
CLIENT_SECRET = "YOUR_GOOGLE_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8501"  # update with your deployed Streamlit URL

AUTHORIZATION_URL = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

API_BASE = "https://homier.vercel.app/users"

st.set_page_config(page_title="Delete Account - Homier", page_icon="🗑️")

st.image("logo_main.png", width=150)
st.title("Delete Your Homier Account")

# Step 1: Google Login
if "token" not in st.session_state:
    oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope="openid email profile", redirect_uri=REDIRECT_URI)
    authorization_url, state = oauth.create_authorization_url(AUTHORIZATION_URL)
    st.write("Please login with Google to continue:")
    st.markdown(f"[Login with Google]({authorization_url})")

else:
    # Step 2: Get user info
    token = st.session_state["token"]
    oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, token=token)
    resp = oauth.get(USER_INFO_URL)
    user_info = resp.json()
    email = user_info.get("email")

    st.success(f"✅ Logged in as {email}")

    # Step 3: Delete Account
    if st.button("Delete My Account"):
        try:
            response = requests.delete(f"{API_BASE}/{email}")
            if response.status_code == 200:
                st.success("✅ Your account has been successfully deleted. We're sad to see you leave, but thank you for being part of Homier.")
            elif response.status_code == 422:
                st.error("⚠️ Invalid email format. Please try again.")
            else:
                st.error("❌ We could not delete your account at this time. Please try again later or contact support.")
        except Exception as e:
            st.error("⚠️ Something went wrong. Please try again.")
