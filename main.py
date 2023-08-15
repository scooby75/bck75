import streamlit as st
from firebase_setup import initialize_firebase
from login_page import login_page
from content_page import content_page

def main():
    st.set_page_config(page_title="App com Streamlit e Firebase")
    auth = initialize_firebase()
    user = login_page(auth)
    content_page(user)

if __name__ == "__main__":
    main()
