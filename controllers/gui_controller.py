import streamlit as st
from models.artist import Artist
from view.view import main_screen, bar_page, theater_page, philanthropic_page, buy_ticket
from models.bar import Bar
from models.theater import Theater
from models.philanthropic import Philanthropic
from controllers.system_controller import SystemController


# Relacion entre las funciones de las clases y el view (la parte grafica)
class GuiController(SystemController):

    # Se asegura que solo exista una unica instancia de la clase GuiController
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = SystemController.__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    def __init__(self):
        super().__init__()
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

            elif st.session_state['page'] == 'theater_event':
                theater_page(gui_controller_obj)

            elif st.session_state['page'] == "philanthropic_event":
                philanthropic_page(gui_controller_obj)

            elif st.session_state['page'] == "buy_ticket":
                buy_ticket(gui_controller_obj)

    # Crea los artistas con su información que participan en cada evento y los almacena en un diccionario
    @staticmethod
    def create_artist(artist_name, artist_price, artist_time):

        artist_obj = Artist(artist_name, artist_price, artist_time)

        # Retorna el objeto creado para el artista
        return artist_obj

    @staticmethod
    def create_bar_event(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price, artist_info):

        # Crea un estado para almacenar los diccionarios de los eventos (solo en caso de que no este creado)
        if 'dictionary' not in st.session_state:
            st.session_state['dictionary'] = {'bar_record': {}}

        # Si no existe en el diccionario, lo añade
        elif 'bar_record' not in st.session_state['dictionary']:
            st.session_state['dictionary']['bar_record'] = {}

        try:

            # Crea el evento de la clase bar con toda la información
            bar_event_obj = Bar(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price, artist_info)

            # Agregar un valor al diccionario
            SystemController.add_dictionary('bar_record', event_name, bar_event_obj)
            st.session_state['dictionary']['bar_record'][event_name] = bar_event_obj

            ans = True

        except ValueError:
            ans = False

        return ans

    @staticmethod
    def create_theater_event(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price, artist_info, theater_rental):

        if 'dictionary' not in st.session_state:
            st.session_state['dictionary'] = {'theater_record': {}}

        elif 'theater_record' not in st.session_state['dictionary']:
            st.session_state['dictionary']['theater_record'] = {}

        try:

            # Crea el evento de la clase bar con toda la información
            theater_event_obj = Theater(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price, artist_info, theater_rental)

            # Agregar un valor al diccionario
            SystemController.add_dictionary('theater_record', event_name, theater_event_obj)
            st.session_state['dictionary']['theater_record'][event_name] = theater_event_obj

            ans = True

        except ValueError:
            ans = False

        return ans

    @staticmethod
    def create_philanthropic_event(event_name, event_date, opening, show_time, place, address, city, event_status, artist_info, sponsors):

        if 'dictionary' not in st.session_state:
            st.session_state['dictionary'] = {'philanthropic_record': {}}

        elif 'philanthropic_record' not in st.session_state['dictionary']:
            st.session_state['dictionary']['philanthropic_record'] = {}

        try:

            # Crea el evento de la clase bar con toda la información
            philanthropic_event_obj = Philanthropic(event_name, event_date, opening, show_time, place, address, city, event_status, artist_info, sponsors)

            # Agregar un valor al diccionario (se utiliza la herencia)
            SystemController.add_dictionary('philanthropic_record', event_name, philanthropic_event_obj)
            st.session_state['dictionary']['philanthropic_record'][event_name] = philanthropic_event_obj

            ans = True

        except ValueError:
            ans = False

        return ans

    @staticmethod
    def get_dictionary(dict_name):

        # Obtener el diccionario para utiliza la información fuera de la clase
        dictionary = SystemController.get_diccionario(dict_name)

        return dictionary
