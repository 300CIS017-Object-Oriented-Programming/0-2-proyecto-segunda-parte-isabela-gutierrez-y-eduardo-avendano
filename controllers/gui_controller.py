import streamlit as st
from models.artist import Artist
from models.user import User
from view.view import main_screen, bar_page, theater_page, philanthropic_page, buy_ticket, modify_page, record_page, report_page
from models.bar import Bar
from models.theater import Theater
from models.philanthropic import Philanthropic
from controllers.system_controller import SystemController
from reportlab.pdfgen import canvas  # Libreria para generar el PDF
from io import BytesIO


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
            main_screen()

        else:

            # Mostrar la principal en caso de que ese sea el estado actual
            if st.session_state['page'] == "show_view":
                main_screen()

            # Si el boton que realizar el cambio de estado de la pagina fue presionado
            elif st.session_state['page'] == "bar_event":
                bar_page(gui_controller_obj)

            elif st.session_state['page'] == 'theater_event':
                theater_page(gui_controller_obj)

            elif st.session_state['page'] == "philanthropic_event":
                philanthropic_page(gui_controller_obj)

            elif st.session_state['page'] == "buy_ticket":
                buy_ticket(gui_controller_obj)

            elif st.session_state['page'] == "modify":
                modify_page(gui_controller_obj)

            elif st.session_state['page'] == "record":
                record_page(gui_controller_obj)

            elif st.session_state['page'] == "report":
                report_page(gui_controller_obj)

    # Crea los artistas con su información que participan en cada evento y los almacena en un diccionario
    @staticmethod
    def create_artist(artist_name, artist_price, artist_time):

        artist_obj = Artist(artist_name, artist_price, artist_time)

        # Retorna el objeto creado para el artista
        return artist_obj

    @staticmethod
    def create_bar_event(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price, artist_info, capacity, sales_phase):

        # Crea un estado para almacenar los diccionarios de los eventos (solo en caso de que no este creado)
        if 'dictionary' not in st.session_state:
            st.session_state['dictionary'] = {'bar_record': {}}

        # Si no existe en el diccionario, lo añade
        elif 'bar_record' not in st.session_state['dictionary']:
            st.session_state['dictionary']['bar_record'] = {}

        try:

            # Crea el evento de la clase bar con toda la información
            bar_event_obj = Bar(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price, artist_info, capacity)
            bar_event_obj.set_sales_phase(sales_phase)

            # Agregar un valor al diccionario
            SystemController.add_dictionary('bar_record', event_name, bar_event_obj)
            st.session_state['dictionary']['bar_record'][event_name] = bar_event_obj

            ans = True

        except ValueError:
            ans = False

        return ans

    @staticmethod
    def create_theater_event(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price, artist_info, theater_rental, capacity, sales_phase):

        if 'dictionary' not in st.session_state:
            st.session_state['dictionary'] = {'theater_record': {}}

        elif 'theater_record' not in st.session_state['dictionary']:
            st.session_state['dictionary']['theater_record'] = {}

        try:

            # Crea el evento de la clase bar con toda la información
            theater_event_obj = Theater(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price, artist_info, theater_rental, capacity)
            theater_event_obj.set_sales_phase(sales_phase)

            # Agregar un valor al diccionario
            SystemController.add_dictionary('theater_record', event_name, theater_event_obj)
            st.session_state['dictionary']['theater_record'][event_name] = theater_event_obj

            ans = True

        except ValueError:
            ans = False

        return ans

    @staticmethod
    def create_philanthropic_event(event_name, event_date, opening, show_time, place, address, city, event_status, artist_info, sponsors, capacity):

        if 'dictionary' not in st.session_state:
            st.session_state['dictionary'] = {'philanthropic_record': {}}

        elif 'philanthropic_record' not in st.session_state['dictionary']:
            st.session_state['dictionary']['philanthropic_record'] = {}

        try:

            # Crea el evento de la clase bar con toda la información
            philanthropic_event_obj = Philanthropic(event_name, event_date, opening, show_time, place, address, city, event_status, artist_info, sponsors, capacity)

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

    # Crea los objetos de los nuevos usuarios
    @staticmethod
    def new_user(name, last_name, user_id, user_mail, event_name, reason, discount):

        try:
            # Llama al constructor de la clase para crear el objeto
            user_obj = User(name, last_name, user_id, user_mail, reason, False)

            if st.session_state['event_type'] == 'bar_event':

                # Accede al evento ya creado
                bar_obj = st.session_state['dictionary']['bar_record'][event_name]

                # Llama a una función para añadir compradores a ese evento
                bar_obj.set_users(name, user_obj)
                sales_phase = bar_obj.get_sales_phase()

                if sales_phase == 'Preventa':
                    bar_obj.add_pre_sale_ticket()
                else:
                    bar_obj.add_regular_sales_ticket()

                bar_obj.add_ticket()

                # Obtiene valores para asginar la utilidad
                ticket_price = bar_obj.get_ticket_price() - (bar_obj.get_ticket_price() * (discount / 100))

                # Asigna la utilidad del bar
                total_bar = ticket_price * 0.2
                bar_obj.set_utility(total_bar)

                # Asgina la utilidad a los artistas
                artist_dict = bar_obj.get_artist_info()

                total_art = (ticket_price * 0.8) / len(artist_dict)

                # El _, ignora la clave, ya que no es utiliza y solo obtiene el valor
                for _, value in artist_dict.items():
                    value.set_utility(total_art)

            if st.session_state['event_type'] == 'theater_event':

                theater_obj = st.session_state['dictionary']['theater_record'][event_name]

                # Llama a una función para añadir compradores a ese evento
                theater_obj.set_users(name, user_obj)
                sales_phase = theater_obj.get_sales_phase()

                if sales_phase == 'Preventa':
                    theater_obj.add_pre_sale_ticket()
                else:
                    theater_obj.add_regular_sales_ticket()

                theater_obj.add_ticket()

                # Obtiene valores para asginar la utilidad
                ticket_price = theater_obj.get_ticket_price()

                # Asigna la utilidad del bar
                total_theater = ticket_price * 0.07
                theater_obj.set_utility(total_theater)

            if st.session_state['event_type'] == "philanthropic_event":

                phil_obj = st.session_state['dictionary']['philanthropic_record'][event_name]
                phil_obj.set_users(name, user_obj)
                phil_obj.add_ticket()

            ans = True

        except ValueError:

            ans = False

        return ans

    # Retorna el estado actual del evento
    @staticmethod
    def get_status(event_name):

        ans = ""

        # Ingresar el objeto del evento para obtener la información
        if st.session_state['event_type'] == 'bar_event':
            bar_obj = st.session_state['dictionary']['bar_record'][event_name]
            ans = bar_obj.get_status()

        if st.session_state['event_type'] == 'theater_event':
            theater_obj = st.session_state['dictionary']['theater_record'][event_name]
            ans = theater_obj.get_status()

        if st.session_state['event_type'] == 'philanthropic_event':
            phil_obj = st.session_state['dictionary']['philanthropic_record'][event_name]
            ans = phil_obj.get_status()

        return ans

    # Le asigna un nuevo estado al evento
    @staticmethod
    def set_status(new_status, event_name):

        ans = True
        try:
            if st.session_state['event_type'] == 'bar_event':
                bar_obj = st.session_state['dictionary']['bar_record'][event_name]
                bar_obj.set_status(new_status)

            if st.session_state['event_type'] == 'theater_event':
                theater_obj = st.session_state['dictionary']['theater_record'][event_name]
                theater_obj.set_status(new_status)

            if st.session_state['event_type'] == 'philanthropic_event':
                phil_obj = st.session_state['dictionary']['philanthropic_record'][event_name]
                phil_obj.set_status(new_status)

        except ValueError:
            ans = False

        return ans

    # Retorna el número de boletas vendidas
    @staticmethod
    def get_sold(event_name):

        ans = 0

        if st.session_state['event_type'] == 'bar_event':
            bar_obj = st.session_state['dictionary']['bar_record'][event_name]
            ans = bar_obj.get_tickets_sold()

        if st.session_state['event_type'] == 'theater_event':
            theater_obj = st.session_state['dictionary']['theater_record'][event_name]
            ans = theater_obj.get_tickets_sold()

        if st.session_state['event_type'] == 'philanthropic_event':
            phil_obj = st.session_state['dictionary']['philanthropic_record'][event_name]
            ans = phil_obj.get_tickets_sold()

        return ans

    @staticmethod
    def delete_event(event_name):

        ans = True
        try:
            # Ingresar al diccionario donde estan los eventos para eliminarlo
            if st.session_state['event_type'] == 'bar_event':

                st.write(st.session_state['dictionary']['bar_record'][event_name])

                st.session_state['dictionary']['bar_record'].pop(event_name)

            if st.session_state['event_type'] == 'theater_event':
                st.session_state['dictionary']['theater_record'].pop(event_name)

            if st.session_state['event_type'] == 'philanthropic_event':
                st.session_state['dictionary']['philanthropic_record'].pop(event_name)

        except ValueError:
            ans = False

        return ans

    # Obtener el aforo maximo del evento
    @staticmethod
    def get_capacity(event_name):

        ans = 0

        # Ingresar el objeto del evento para obtener la información
        if st.session_state['event_type'] == 'bar_event':
            bar_obj = st.session_state['dictionary']['bar_record'][event_name]
            ans = bar_obj.get_capacity()

        if st.session_state['event_type'] == 'theater_event':
            theater_obj = st.session_state['dictionary']['theater_record'][event_name]
            ans = theater_obj.get_capacity()

        if st.session_state['event_type'] == 'philanthropic_event':
            phil_obj = st.session_state['dictionary']['philanthropic_record'][event_name]
            ans = phil_obj.get_capacity()

        return ans

    # Generar el PDF para imprimirlo
    @staticmethod
    def create_pdf(event_name, username):

        event_date, place, user_first_name, user_last_name, user_id, user_email = None, None, None, None, None, None

        # Asignar toda la información que se va a imprimir
        if st.session_state['event_type'] == 'bar_event':
            obj = st.session_state['dictionary']['bar_record'][event_name]
            place = obj.get_place()
            users_dict = obj.get_users()

            user_obj = None
            if username in users_dict:
                user_obj = users_dict[username]

            user_first_name = user_obj.get_first_name()
            user_last_name = user_obj.get_last_name()
            user_id = user_obj.get_identification()
            user_email = user_obj.get_email()

        if st.session_state['event_type'] == 'theater_event':
            obj = st.session_state['dictionary']['theater_record'][event_name]
            place = obj.get_place()
            users_dict = obj.get_users()

            user_obj = None
            if username in users_dict:
                user_obj = users_dict[username]

            user_first_name = user_obj.get_first_name()
            user_last_name = user_obj.get_last_name()
            user_id = user_obj.get_identification()
            user_email = user_obj.get_email()

        if st.session_state['event_type'] == 'philanthropic_event':

            obj = st.session_state['dictionary']['philanthropic_record'][event_name]
            place = obj.get_place()
            users_dict = obj.get_users()

            user_obj = None
            if username in users_dict:
                user_obj = users_dict[username]

            user_first_name = user_obj.get_first_name()
            user_last_name = user_obj.get_last_name()
            user_id = user_obj.get_identification()
            user_email = user_obj.get_email()

        # Almacena los datos en forma de bytes
        buffer = BytesIO()

        # Se crea la hoja en blanco con una clase
        c = canvas.Canvas(buffer)

        # Imprime información
        c.drawString(100, 750, event_name)
        c.drawString(100, 760, place)
        c.drawString(100, 770, user_first_name)
        c.drawString(100, 780, user_last_name)
        c.drawString(100, 790, user_id)
        c.drawString(100, 800, user_email)

        # Guarda el contenido
        c.save()

        # Retorna los bytes del PDF generado
        pdf_bytes = buffer.getvalue()

        return pdf_bytes

    @staticmethod
    def change_attendance(event_name, username):

        ans = True
        try:
            if st.session_state['event_type'] == 'bar_event':
                obj = st.session_state['dictionary']['bar_record'][event_name]
                users_dict = obj.get_users()

                user_obj = None
                if username in users_dict:
                    user_obj = users_dict[username]

                user_obj.set_attendance(True)

            if st.session_state['event_type'] == 'theater_event':
                obj = st.session_state['dictionary']['theater_record'][event_name]
                users_dict = obj.get_users()

                user_obj = None
                if username in users_dict:
                    user_obj = users_dict[username]

                user_obj.set_attendance(True)

            if st.session_state['event_type'] == 'philanthropic_event':
                obj = st.session_state['dictionary']['philanthropic_record'][event_name]
                users_dict = obj.get_users()

                user_obj = None
                if username in users_dict:
                    user_obj = users_dict[username]

                user_obj.set_attendance(True)

        except ValueError:
            ans = False

        return ans

    @staticmethod
    def get_pre_sale_ticket(event_name):

        ans = 0

        if st.session_state['event_type'] == 'bar_event':
            bar_obj = st.session_state['dictionary']['bar_record'][event_name]
            ans = bar_obj.get_pre_sale_tickets()

        if st.session_state['event_type'] == 'theater_event':
            theater_obj = st.session_state['dictionary']['theater_record'][event_name]
            ans = theater_obj.get_pre_sale_tickets()

        if st.session_state['event_type'] == 'philanthropic_event':
            phil_obj = st.session_state['dictionary']['philanthropic_record'][event_name]
            ans = phil_obj.get_pre_sale_tickets()

        return ans

    @staticmethod
    def get_regular_sales_tickets(event_name):

        ans = 0

        if st.session_state['event_type'] == 'bar_event':
            bar_obj = st.session_state['dictionary']['bar_record'][event_name]
            ans = bar_obj.get_regular_sales_tickets()

        if st.session_state['event_type'] == 'theater_event':
            theater_obj = st.session_state['dictionary']['theater_record'][event_name]
            ans = theater_obj.get_regular_sales_tickets()

        if st.session_state['event_type'] == 'philanthropic_event':
            phil_obj = st.session_state['dictionary']['philanthropic_record'][event_name]
            ans = phil_obj.get_regular_sales_tickets()

        return ans
