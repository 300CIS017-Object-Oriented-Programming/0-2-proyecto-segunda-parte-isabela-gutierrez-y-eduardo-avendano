import streamlit as st
from view.view import main_screen, bar_page


def call_functions():

    if 'page' not in st.session_state:
        st.session_state['page'] = "show_view"
        main_screen()
    else:
        if st.session_state['page'] == "show_view":
            main_screen()
        elif st.session_state['page'] == "bar_event":
            bar_page()
0