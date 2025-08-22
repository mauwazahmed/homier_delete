import streamlit as st
import requests

API_BASE = "https://homier.vercel.app/users"

st.set_page_config(page_title="Account Deletion", page_icon="🗑️")

st.title("🗑️ Account Deletion Portal")
st.write("Enter your email below to view or delete your account data.")

email = st.text_input("Enter your email")

if email:
    # Show user details
    if st.button("Get User Details"):
        try:
            response = requests.get(f"{API_BASE}/{email}")
            if response.status_code == 200:
                st.success("✅ User details fetched successfully!")
                st.json(response.json())
            elif response.status_code == 422:
                st.error("⚠️ Invalid email format. Please enter a valid email.")
            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"⚠️ Request failed: {e}")

    # Delete user account
    if st.button("Delete Account"):
        try:
            response = requests.delete(f"{API_BASE}/{email}")
            if response.status_code == 200:
                st.success("✅ Account deleted successfully.")
            elif response.status_code == 422:
                st.error("⚠️ Invalid email format. Please enter a valid email.")
            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"⚠️ Request failed: {e}")
