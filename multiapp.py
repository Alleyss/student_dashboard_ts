import streamlit as st
from streamlit_option_menu import option_menu

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        # Sidebar menu
        with st.sidebar:
            app_selection = option_menu(
                menu_title='Student Dashboard',
                options=[app["title"] for app in self.apps],  # Dynamically load options from the apps list
                icons=['house-fill', 'building', 'book', 'person-fill', 'person-circle', 'file-earmark', 
                       'calendar-check', 'bell', 'envelope', 'box-arrow-right'],
                menu_icon='list',
                default_index=0,
                styles={
                    "container": {"padding": "2!important", "background-color": 'black'},
                    "icon": {"color": "white", "font-size": "23px"},
                    "nav-link": {"color": "white", "font-size": "20px", "text-align": "left", "margin": "0px", "--hover-color": "blue"},
                    "nav-link-selected": {"background-color": "#02ab21"},
                }
            )

        # Run the corresponding function based on the selected app
        for app in self.apps:
            if app["title"] == app_selection:
                app["function"]()

    def logout():
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.write("You have logged out successfully.")
        st.rerun()
      # Refresh the app to show login page again
