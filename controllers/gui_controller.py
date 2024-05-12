import streamlit as st
from models.artist import Artist
from view.view import main_screen, bar_page, theater_page
from models.bar import Bar
from controllers.system_controller import SystemController


# Relacion entre las funciones de las clases y el view (la parte grafica)
class GuiController:

    # Se asegura que solo exista una unica instancia de la clase GuiController
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        self.__initialized = True

    # Es un metodo estatico ya que no se modifica ninguna variable (no modifica nada)
    @staticmethod
    # Se encarga de administrar cuando se muestan las paginas, dependiendo de los botones
    def call_functions():

        # Declaración de la clase GuiController
        gui_controller_obj = GuiController()

        # Si la pagina no se encuentra en la principal
        if 'page' not in st.session_state:

            # La sesión de estados page maneja que pagina se muestra en el momento actual
            st.session_state['page'] = "show_view"
            main_screen(gui_controller_obj)

        else:

            # Mostrar la principal en caso de que ese sea el estado actual
            if st.session_state['page'] == "show_view":
                main_screen(gui_controller_obj)

            # Si el boton que realizar el cambio de estado de la pagina fue presionado
            elif st.session_state['page'] == "bar_event":
                bar_page(gui_controller_obj)

            elif st.session_state['page'] == "theater_event":
                theater_page(gui_controller_obj)

    # Crea los artistas con su información que participan en cada evento y los almacena en un diccionario
    @staticmethod
    def create_artist(artist_name, artist_price, artist_time):

        artist_obj = Artist(artist_name, artist_price, artist_time)

        # Retorna el objeto creado para el artista
        return artist_obj

    @staticmethod
    def create_bar_event(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price, artist_info):

        # Declaración de una variable para hacer referencia a un objeto de la clase SystemController
        system_obj = SystemController()

        # Crea un estado para almacenar los mapas de los eventos (solo en caso de que no este creado)
        if 'dictionary' not in st.session_state:

            # Crea el diccionario y asigna que el interno no existe
            st.session_state['dictionary'] = {'bar_record': {}, 'bar_record_created': False}

        elif st.session_state['dictionary']['bar_record'] is False:

            # Verifica si el interno ya fue creado
            if not st.session_state['dictionary']['bar_record_created']:

                # Si no ha sido creado, lo crea y lo marca como existente
                st.session_state['dictionary']['bar_record'] = {}
                st.session_state['dictionary']['bar_record_created'] = True

        try:

            # Crea el evento de la clase bar con toda la información
            bar_event_obj = Bar(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price, artist_info)

            # Agregar un valor al diccionario
            system_obj.add_dictionary('bar_record', event_name, bar_event_obj)
            st.session_state['dictionary']['bar_record'][event_name] = bar_event_obj

            ans = True

        except ValueError:
            ans = False

        return ans

    @staticmethod
    def get_dictionary(dict_name):

        system_obj = SystemController()

        # Obtener el diccionario para utiliza la información fuera de la clase
        dictionary = system_obj.get_diccionario(dict_name)

        return dictionary
