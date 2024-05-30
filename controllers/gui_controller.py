import streamlit as st
from models.artist import Artist
from models.user import User
from view.view import main_screen, bar_page, theater_page, philanthropic_page, buy_ticket, modify_page, record_page, report_page, report_by_artist, dashboard
from models.bar import Bar
from models.theater import Theater
from models.ticket import Ticket
from models.philanthropic import Philanthropic
from controllers.system_controller import SystemController
import plotly.express as px  # Libreria para hacer las graficas
import pandas as pd

# Librerias para el manejo del PDF
from io import BytesIO
from reportlab.pdfgen import canvas


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

            elif st.session_state['page'] == "report_by_artist":
                report_by_artist(gui_controller_obj)

            elif st.session_state['page'] == "dashboard":
                dashboard(gui_controller_obj)

    # Crea los artistas con su información que participan en cada evento y los almacena en un diccionario
    @staticmethod
    def create_artist(artist_name, artist_price, artist_time):

        artist_obj = Artist(artist_name, artist_price, artist_time)

        # Retorna el objeto creado para el artista
        return artist_obj

    # Crea los eventos de tipo bar con su respectiva información
    @staticmethod
    def create_bar_event(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price_pre_sale, ticket_regular, artist_info, capacity):

        # Crea un estado para almacenar los diccionarios de los eventos (solo en caso de que no este creado)
        if 'dictionary' not in st.session_state:
            st.session_state['dictionary'] = {'bar_record': {}}

        # Si no existe en el diccionario, lo añade
        elif 'bar_record' not in st.session_state['dictionary']:
            st.session_state['dictionary']['bar_record'] = {}

        try:

            # Crear un objeto con toda la informacion de la tiqueteria
            ticket_obj = Ticket(ticket_price_pre_sale, ticket_regular)

            # Crea el evento de la clase bar con toda la información
            bar_event_obj = Bar(event_name, event_date, opening, show_time, place, address, city, event_status, artist_info, capacity, ticket_obj)

            # Agregar un valor al diccionario
            SystemController.add_dictionary('bar_record', event_name, bar_event_obj)
            st.session_state['dictionary']['bar_record'][event_name] = bar_event_obj

            ans = True

        except ValueError:
            ans = False

        return ans

    # Crea los eventos del teatro con su informacion
    @staticmethod
    def create_theater_event(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price_pre_sale, ticket_regular, artist_info, theater_rental, capacity):

        if 'dictionary' not in st.session_state:
            st.session_state['dictionary'] = {'theater_record': {}}

        elif 'theater_record' not in st.session_state['dictionary']:
            st.session_state['dictionary']['theater_record'] = {}

        try:

            # Crear la información de la tiquetera
            ticket_obj = Ticket(ticket_price_pre_sale, ticket_regular)

            # Crea el evento de la clase bar con toda la información
            theater_event_obj = Theater(event_name, event_date, opening, show_time, place, address, city, event_status, artist_info, theater_rental, capacity, ticket_obj)

            # Agregar un valor al diccionario
            SystemController.add_dictionary('theater_record', event_name, theater_event_obj)
            st.session_state['dictionary']['theater_record'][event_name] = theater_event_obj

            ans = True

        except ValueError:
            ans = False

        return ans

    # Crea los eventos de tipo filantropico
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

    # Obtiene el diccionario de un evento para saber su informacion
    @staticmethod
    def get_dictionary(dict_name):

        # Obtener el diccionario para utiliza la información fuera de la clase
        dictionary = SystemController.get_diccionario(dict_name)

        return dictionary

    # Crea los objetos de los nuevos usuarios
    @staticmethod
    def new_user(name, last_name, user_id, user_mail, event_name, reason, sales_phase, payment_method, ticket_price):

        try:
            # Llama al constructor de la clase para crear el objeto
            user_obj = User(name, last_name, user_id, user_mail, reason, False, payment_method, ticket_price, sales_phase)

            if st.session_state['event_type'] == 'bar_event':

                # Accede al evento ya creado
                bar_obj = st.session_state['dictionary']['bar_record'][event_name]

                # Llama a una función para añadir compradores a ese evento
                bar_obj.set_users(name, user_obj)

                # Sumar el tipo de boleta vendida
                bar_obj.add_ticket(sales_phase)

                if sales_phase == "Preventa":
                    bar_obj.set_total_sale_phase("Preventa", ticket_price)
                elif sales_phase == "Venta regular":
                    bar_obj.set_total_sale_phase("Venta regular", ticket_price)

                # Asigna el dinero ingresado a su respectivo medio de pago
                if payment_method == "Tarjeta":
                    bar_obj.add_total_card(ticket_price, sales_phase)
                elif payment_method == "Efectivo":
                    bar_obj.add_total_cash(ticket_price, sales_phase)

                bar_obj.set_total_money(ticket_price)
                total_money = bar_obj.get_total_money()

                # Asigna la utilidad del bar
                total_bar = total_money * 0.2
                bar_obj.set_utility(total_bar)

                # Asgina la utilidad a los artistas
                artist_dict = bar_obj.get_artist_info()
                total_art = (total_money * 0.8) / len(artist_dict)

                # El _, ignora la clave, ya que no es utiliza y solo obtiene el valor
                for _, value in artist_dict.items():
                    value.set_utility(total_art)

            if st.session_state['event_type'] == 'theater_event':

                theater_obj = st.session_state['dictionary']['theater_record'][event_name]

                # Llama a una función para añadir compradores a ese evento
                theater_obj.set_users(name, user_obj)
                theater_obj.add_ticket(sales_phase)

                if sales_phase == "Preventa":
                    theater_obj.set_total_sale_phase("Preventa", ticket_price)
                elif sales_phase == "Venta regular":
                    theater_obj.set_total_sale_phase("Venta regular", ticket_price)

                # Asigna el dinero ingresado a su respectivo medio de pago
                if payment_method == "Tarjeta":
                    theater_obj.add_total_card(ticket_price, sales_phase)
                elif payment_method == "Efectivo":
                    theater_obj.add_total_cash(ticket_price, sales_phase)

                theater_obj.set_total_money(ticket_price)
                total_money = theater_obj.get_total_money()

                # Asigna la utilidad del bar
                total_theater = total_money * 0.07
                theater_obj.set_utility(total_theater)

            if st.session_state['event_type'] == "philanthropic_event":

                phil_obj = st.session_state['dictionary']['philanthropic_record'][event_name]
                phil_obj.set_users(name, user_obj)
                phil_obj.add_ticket("N/A")

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

    # Elimina los eventos que no tienen boleteria vendida
    @staticmethod
    def delete_event(event_name):

        ans = True
        try:
            # Ingresar al diccionario donde estan los eventos para eliminarlo
            if st.session_state['event_type'] == 'bar_event':
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

        event_date, place, user_first_name, user_last_name, user_id, user_email, user_ticket, user_payment = None, None, None, None, None, None, None, None

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
            user_ticket = str(user_obj.get_ticket_price())
            user_payment = str(user_obj.get_payment_method())

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
            user_ticket = str(user_obj.get_ticket_price())
            user_payment = str(user_obj.get_payment_method())

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
            user_ticket = str(user_obj.get_ticket_price())
            user_payment = str(user_obj.get_payment_method())

        # Almacena los datos en forma de bytes
        buffer = BytesIO()

        # Se crea la hoja en blanco con una clase
        c = canvas.Canvas(buffer)

        # Agrega título y separador
        c.setFont("Helvetica-Bold", 20)
        c.drawString(100, 800, "Boleto de Entrada")
        c.line(100, 790, 500, 790)

        # Imprime información del evento
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 760, "Evento:")
        c.setFont("Helvetica", 14)
        c.drawString(200, 760, event_name)

        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 740, "Lugar:")
        c.setFont("Helvetica", 14)
        c.drawString(200, 740, place)

        # Imprime información del usuario
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 720, "Nombre:")
        c.setFont("Helvetica", 14)
        c.drawString(200, 720, f"{user_first_name} {user_last_name}")

        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 700, "ID:")
        c.setFont("Helvetica", 14)
        c.drawString(200, 700, user_id)

        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 680, "Email:")
        c.setFont("Helvetica", 14)
        c.drawString(200, 680, user_email)

        # Imprime información adicional
        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 660, "Precio del Boleto:")
        c.setFont("Helvetica", 14)
        c.drawString(260, 660, user_ticket)

        c.setFont("Helvetica-Bold", 14)
        c.drawString(100, 640, "Método de Pago:")
        c.setFont("Helvetica", 14)
        c.drawString(260, 640, user_payment)

        # Guarda el contenido
        c.save()

        # Retorna los bytes del PDF generado
        pdf_bytes = buffer.getvalue()

        return pdf_bytes

    # Realiza el registro de asistencia de las personas que compran boletas
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

    # Retorna el numero de boletas de preventa vendidas
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

    # Retorna el numero de boletas de venta regular vendidas
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

    # Retorna los precios de ambos tipos de boletas
    @staticmethod
    def get_ticket_price(event_name, sales_phase):

        ans = 0
        if sales_phase == "Preventa":
            if st.session_state['event_type'] == 'bar_event':
                bar_obj = st.session_state['dictionary']['bar_record'][event_name]
                ans = bar_obj.get_ticket_price("Preventa")

            if st.session_state['event_type'] == 'theater_event':
                theater_obj = st.session_state['dictionary']['theater_record'][event_name]
                ans = theater_obj.get_ticket_price("Preventa")

            if st.session_state['event_type'] == 'philanthropic_event':
                phil_obj = st.session_state['dictionary']['philanthropic_record'][event_name]
                ans = phil_obj.get_ticket_price("Preventa")

        else:
            if st.session_state['event_type'] == 'bar_event':
                bar_obj = st.session_state['dictionary']['bar_record'][event_name]
                ans = bar_obj.get_ticket_price("Venta regular")

            if st.session_state['event_type'] == 'theater_event':
                theater_obj = st.session_state['dictionary']['theater_record'][event_name]
                ans = theater_obj.get_ticket_price("Venta regular")

            if st.session_state['event_type'] == 'philanthropic_event':
                phil_obj = st.session_state['dictionary']['philanthropic_record'][event_name]
                ans = phil_obj.get_ticket_price("Venta regular")

        return ans

    # Retorna las ganancias del medio de pago en efectivo
    @staticmethod
    def get_cash(event_name, sales_phase):

        ans = 0

        if st.session_state['event_type'] == 'bar_event':
            bar_obj = st.session_state['dictionary']['bar_record'][event_name]
            ans = bar_obj.get_total_cash(sales_phase)

        if st.session_state['event_type'] == 'theater_event':
            theater_obj = st.session_state['dictionary']['theater_record'][event_name]
            ans = theater_obj.get_total_cash(sales_phase)

        return ans

    # Retorna las ganancias del medio de pago con tarjeta
    @staticmethod
    def get_card(event_name, sales_phase):

        ans = 0

        if st.session_state['event_type'] == 'bar_event':
            bar_obj = st.session_state['dictionary']['bar_record'][event_name]
            ans = bar_obj.get_total_card(sales_phase)

        if st.session_state['event_type'] == 'theater_event':
            theater_obj = st.session_state['dictionary']['theater_record'][event_name]
            ans = theater_obj.get_total_card(sales_phase)

        return ans

    # Retorna el diccionario con compradores de un respectivo evento
    @staticmethod
    def get_dict_users(event_name):

        ans = {}

        if st.session_state['event_type'] == 'bar_event':
            bar_obj = st.session_state['dictionary']['bar_record'][event_name]
            ans = bar_obj.get_users()

        if st.session_state['event_type'] == 'theater_event':
            theater_obj = st.session_state['dictionary']['theater_record'][event_name]
            ans = theater_obj.get_users()

        if st.session_state['event_type'] == 'philanthropic_event':
            phil_obj = st.session_state['dictionary']['philanthropic_record'][event_name]
            ans = phil_obj.get_users()

        return ans

    # Retorna el diccionario con los artistas de un evento especifico
    @staticmethod
    def get_dict_artist(event_name):

        ans = {}
        if st.session_state['event_type'] == 'bar_event':
            bar_obj = st.session_state['dictionary']['bar_record'][event_name]
            ans = bar_obj.get_artist_info()

        if st.session_state['event_type'] == 'theater_event':
            theater_obj = st.session_state['dictionary']['theater_record'][event_name]
            ans = theater_obj.get_artist_info()

        if st.session_state['event_type'] == 'philanthropic_event':
            phil_obj = st.session_state['dictionary']['philanthropic_record'][event_name]
            ans = phil_obj.get_artist_info()

        return ans

    # Realiza las tablas y graficas con la informacion
    @staticmethod
    def graphics(event_name):

        users = {}
        if st.session_state['event_type'] == 'bar_event':
            bar_obj = st.session_state['dictionary']['bar_record'][event_name]
            users = bar_obj.get_users()

        if st.session_state['event_type'] == 'theater_event':
            theater_obj = st.session_state['dictionary']['theater_record'][event_name]
            users = theater_obj.get_users()

        if st.session_state['event_type'] == 'philanthropic_event':
            phil_obj = st.session_state['dictionary']['philanthropic_record'][event_name]
            users = phil_obj.get_users()

        # Reune el número de boletas por cada tipo y los metodos de pago
        num_pre_sale, num_regular, num_card, num_cash = 0, 0, 0, 0
        for value in users.values():

            if value.get_sale_phase() == 'Preventa':
                num_pre_sale += 1
            elif value.get_sale_phase() == 'Venta regular':
                num_regular += 1

            if value.get_payment_method() == 'Efectivo':
                num_cash += 1
            elif value.get_payment_method() == 'Tarjeta':
                num_card += 1

        data_sale = {
            'Tipo de boleta': ['Preventa', 'Venta regular'],
            'Boletas vendidas': [num_pre_sale, num_regular]
        }

        data_pay = {
            'Metodo de pago': ['Efectivo', 'Tarjeta'],
            'Tipo de compra': [num_cash, num_card]
        }

        # Crea los datos
        dfs = pd.DataFrame(data_sale)
        dfp = pd.DataFrame(data_pay)

        # Crea un gráfico de barras con Plotly
        fig_sale = px.bar(dfs, x = 'Tipo de boleta', y = 'Boletas vendidas', title = 'Compra de boletas')
        fig_pay = px.bar(dfp, x = 'Metodo de pago', y = 'Tipo de compra', title = 'Medios de pago')

        return fig_sale, fig_pay, dfs, dfp

    # Convierte en un tipo de Excel para descargar
    @staticmethod
    def to_excel(df):

        with BytesIO() as output:
            with pd.ExcelWriter(output, engine = 'xlsxwriter') as writer:
                df.to_excel(writer, index = False, sheet_name = 'Sheet1')
            processed_data = output.getvalue()

        return processed_data

    # Busca un evento por el nombre del artista
    @staticmethod
    def find_event(art_name):

        dictionary = st.session_state['dictionary']

        # Recorre el diccionario hasta que coincida con el artista
        for key, value in dictionary.items():
            for key_2, value_2 in value.items():
                art_dict = value_2.get_artist_info()
                for key_3 in art_dict.keys():
                    if key_3 == art_name:
                        return key_2, key

    # Retorna toda la informacion para hacer el reporte
    @staticmethod
    def get_info(event_name):

        date, place, capacity = "", "", 0
        if st.session_state['event_type'] == 'bar_event':
            bar_obj = st.session_state['dictionary']['bar_record'][event_name]
            date = bar_obj.get_event_date()
            place = bar_obj.get_place()
            capacity = bar_obj.get_capacity()

        if st.session_state['event_type'] == 'theater_event':
            theater_obj = st.session_state['dictionary']['theater_record'][event_name]
            date = theater_obj.get_event_date()
            place = theater_obj.get_place()
            capacity = theater_obj.get_capacity()

        if st.session_state['event_type'] == 'philanthropic_event':
            phil_obj = st.session_state['dictionary']['philanthropic_record'][event_name]
            date = phil_obj.get_event_date()
            place = phil_obj.get_place()
            capacity = phil_obj.get_capacity()

        return date, place, capacity

    # Evalua la cantidad de veces que se repite un evento en unas fechas
    @staticmethod
    def update_count():

        count_dict = {}
        diccionarios = st.session_state['dictionary']

        # Recorremos cada diccionario en el diccionario principal
        for d in diccionarios.values():
            for key, obj in d.items():

                event_date = obj.get_event_date()
                event_name = obj.get_event_name()
                total_money = obj.get_total_money()

                event_type = " "
                if st.session_state['event_type'] == 'bar_event':
                    event_type = "Bar"
                elif st.session_state['event_type'] == 'theater_event':
                    event_type = "Theater"
                elif st.session_state['event_type'] == 'philanthropic_event':
                    event_type = "Philanthropic"

                if event_date in count_dict:
                    count_dict[event_date]['count'] += 1
                    count_dict[event_date]['event_name'].append(event_name)
                    count_dict[event_date]['total_money'].append(total_money)
                else:
                    count_dict[event_date] = {'count': 1, 'event_type': event_type, 'event_names': [event_name], 'total_moneys': [total_money]}

        # Convertimos el diccionario auxiliar en una lista de tuplas
        result = [(event_date, data['count'], data['event_type'], data['event_names'], data['total_moneys']) for event_date, data in count_dict.items()]
        return result

    # Dinero total recaudado en un tipo de boleteria
    @staticmethod
    def get_total_phase(sale_phase, event_name):

        ans = 0

        if st.session_state['event_type'] == 'bar_event':
            bar_obj = st.session_state['dictionary']['bar_record'][event_name]
            ans = bar_obj.get_total_sale_phase(sale_phase)

        if st.session_state['event_type'] == 'theater_event':
            theater_obj = st.session_state['dictionary']['theater_record'][event_name]
            ans = theater_obj.get_total_sale_phase(sale_phase)

        return ans
