import streamlit as st
from login_page import login_page
from content_page import content_page

def main():
    st.set_page_config(page_title="App com Streamlit e Firebase")
    
    user = login_page()
    content_page(user)

if __name__ == "__main__":
    main()
