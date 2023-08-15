import streamlit as st
from firebase_setup import auth
from content_page import content_page
from login_page import login_page

def main():
    st.set_page_config(page_title="App com Streamlit e Firebase")
    
    user = login_page()
    content_page(user)

if __name__ == "__main__":
    main()
