import streamlit as st
from settings import TITLE_STYLE, OPTIONS


def main_screen():

    # Asignar titulo y barra superior
    st.markdown(OPTIONS, unsafe_allow_html = True)
    st.markdown(TITLE_STYLE, unsafe_allow_html = True)

    # Crear columnas con su respectiva información
    col1, col2, col3 = st.columns(3)

    # Asignar el contenido de las columnas (imagen y botón)
    with col1:
        st.image("docs/img/evento_bar.jpg", use_column_width = True)

        # Cargar contenido de la pagina del bar
        if st.button("Nuevo evento Bar", use_container_width = True):
            st.session_state['page'] = "bar_event"
            st.rerun()

    with col2:
        st.image("docs/img/evento_teatro.jpg", use_column_width = True)

        if st.button("Nuevo evento Teatro", use_container_width = True):
            st.title("Nuevo evento Teatro")

    with col3:
        st.image("docs/img/evento_filantropico.jpg", use_column_width = True)
        st.button("Nuevo evento Filantropico", use_container_width = True)


def bar_page():
    st.title("Nuevo evento Bar")
