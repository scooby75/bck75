import streamlit as st

from streamlit_option_menu import option_menu


import trending, test, your, about
st.set_page_config(
        page_title="Football Data Analysis",
)



class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
           
        if app == "Account":
            test.app()    
       
             
          
             
    run()    

