import streamlit as st
from controllers.gui_controller import GuiController

# Información en la pestaña
st.set_page_config(page_title = "Gestión de Eventos", page_icon = "📝", layout = "wide", initial_sidebar_state = "expanded")

# Definición de la parte visual de la pagina
controller_obj = GuiController()
controller_obj.call_functions()
