import streamlit as st
from settings import TITLE_STYLE, FOOTER, BAR_TITLE_STYLE, BUTTON_STYLE, TICKET_TITLE, THEATER_TITLE_STYLE, PHILANTHROPIC_TITLE_STYLE, TITLE_MODIFICATION, REGISTRATION_TITLE
from datetime import date  # Muestra el calendario para el registro de fechas
import matplotlib.pyplot as plt
import pandas as pd


# Pagina principal
def main_screen():

    col1, col2, col3, col4, col5, col6 = st.columns(6)

    # Mostrar el estilo de los botones
    st.markdown(BUTTON_STYLE, unsafe_allow_html = True)

    with col1:
        if st.button("Comprar boleta", use_container_width = True):
            st.session_state['page'] = "buy_ticket"
            st.rerun()

    with col2:
        if st.button("Modificar estado", use_container_width = True):
            st.session_state['page'] = "modify"
            st.rerun()

    with col3:
        if st.button("Registrar ingreso", use_container_width = True):
            st.session_state['page'] = "record"
            st.rerun()

    with col4:
        if st.button("Generar reporte", use_container_width = True):
            st.session_state['page'] = "report"
            st.rerun()

    with col5:
        if st.button("Evento por artista", use_container_width = True):
            st.session_state['page'] = "report_by_artist"
            st.rerun()

    with col6:
        if st.button("Dashboard", use_container_width=True):
            st.session_state['page'] = "dashboard"
            st.rerun()

    # Asignar titulo y barra superior
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

        # Cargar contenido de la pagina del teatro
        if st.button("Nuevo evento Teatro", use_container_width = True):
            st.session_state['page'] = "theater_event"
            st.rerun()

    with col3:
        st.image("docs/img/evento_filantropico.jpg", use_column_width = True)

        # Mostrar contenido del evento filantropico
        if st.button("Nuevo evento Filantropico", use_container_width = True):
            st.session_state['page'] = "philanthropic_event"
            st.rerun()

    # Mostrar el pie de pagina
    st.markdown(FOOTER, unsafe_allow_html = True)


# Función para recolectar toda la información
def input_info(gui_controller_obj):

    col1, col2 = st.columns(2)

    with col1:

        # Subtitulo de la columna
        st.markdown("<h3 style = 'text-align: center'> Información evento </h3>", unsafe_allow_html = True)
        event_name = st.text_input("Nombre del evento")

        # Muestra un calendario para seleccionar la fecha del evento
        event_date = st.date_input("Selecciona una fecha", date.today())

        opening = st.text_input("Hora de apertura")
        show_time = st.text_input("Hora del evento")
        place = st.text_input("Lugar del evento")
        address = st.text_input("Dirección del evento")
        city = st.text_input("Ciudad del evento")
        capacity = st.number_input("Capacidad del evento", step = 1)

    with col2:

        st.markdown("<h3 style = 'text-align: center'> Información artista </h3>", unsafe_allow_html = True)
        event_status = st.selectbox("Estado del evento", ["Por realizar", "Realizado" "Cancelado", "Aplazado", "Cerrado"])

        # Ingresa los valores de boleta dependiendo de la fase
        if st.session_state['event_type'] != "philanthropic_event":
            ticket_price_pre_sale = st.number_input("Valor de la boleta en preventa", step = 1)
            ticket_regular_price = st.number_input("Valor de la boleta regular", step = 1)

        # Menú desplegable con el número de artistas
        num_artists = st.selectbox("Numero de artistas", range(1, 5))

        # Pregunta la información para el número de artistas seleccionados
        artist_counter = 0
        artist_info = {}
        while artist_counter < num_artists:

            # Para no generar las mismas claves en las entradas se hace un conteo de artistas
            artist_name = st.text_input(f"Nombre del artista {artist_counter + 1}")
            artist_price = st.text_input(f"Valor del artista {artist_counter + 1}")
            artist_time = st.text_input(f"Hora de presentación del artista {artist_counter + 1}")

            # Crear objeto del artista
            artist_obj_info = gui_controller_obj.create_artist(artist_name, artist_price, artist_time)
            artist_info[artist_name] = artist_obj_info

            artist_counter += 1

    # Llama al constructor de el evento bar si se encuentra en ese estado
    if st.session_state['event_type'] == "bar_event":

        if st.button("Crear evento Bar", use_container_width = True):

            # Se pasan los valores de los parametros para crear el objeto
            init_obj = gui_controller_obj.create_bar_event(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price_pre_sale, ticket_regular_price, artist_info, capacity)

            # Informa al usuario si el evento se creo de manera exitosa
            if init_obj:
                st.success("Evento bar creado exitosamente")
            else:
                st.warning("Evento bar no creado exitosamente")

    if st.session_state['event_type'] == 'theater_event':

        theather_cost = st.text_input("Alquiler del teatro")

        if st.button("Crear evento teatro", use_container_width = True):

            init_obj = gui_controller_obj.create_theater_event(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price_pre_sale, ticket_regular_price, artist_info, theather_cost, capacity)

            # Informa al usuario si el evento se creo de manera exitosa
            if init_obj:
                st.success("Evento teatro creado exitosamente")
            else:
                st.warning("Evento teatro no creado exitosamente")

    if st.session_state['event_type'] == 'philanthropic_event':

        num_sponsor = st.selectbox("Numero de sponsors", range(1, 5))

        cont_sponsor = 0
        dict_sponsor = {}
        while cont_sponsor < num_sponsor:
            sponsor_name = st.text_input("Nombre del patrocinador")
            sponsor_price = st.text_input("Valor del patrocinador")

            dict_sponsor[sponsor_name] = sponsor_price

            cont_sponsor += 1

        if st.button("Crear evento filantropico", use_container_width = True):

            init_obj = gui_controller_obj.create_philanthropic_event(event_name, event_date, opening, show_time, place, address, city, event_status, artist_info, dict_sponsor, capacity)

            # Informa al usuario si el evento se creo de manera exitosa
            if init_obj:
                st.success("Evento filantropico creado exitosamente")
            else:
                st.warning("Evento filantropico no creado exitosamente")

    if st.button("Regresar", use_container_width = True):
        st.session_state['page'] = "show_view"
        st.rerun()


# Funcion para realizar la compra y generación de boletas
def buy_ticket(gui_controller_obj):

    st.session_state['page'] = "buy_ticket"

    st.markdown(TICKET_TITLE, unsafe_allow_html = True)
    select_event = st.radio("Tipo de evento", ['Bar', 'Teatro', 'Filantropico'], index = 0, format_func = lambda x: x.upper())

    # Verifica si ya hay eventos creados en el diccionario
    if 'dictionary' in st.session_state:

        # Imprime todas las opciones de evento que hay en el diccionario
        dictionary = {}
        if select_event == "Bar":
            st.session_state['event_type'] = "bar_event"
            dictionary = gui_controller_obj.get_dictionary("bar_record")
        elif select_event == "Teatro":
            st.session_state['event_type'] = "theater_event"
            dictionary = gui_controller_obj.get_dictionary("theater_record")
        elif select_event == "Filantropico":
            st.session_state['event_type'] = "philanthropic_event"
            dictionary = gui_controller_obj.get_dictionary("philanthropic_record")

        if not dictionary:
            st.write("No hay eventos disponibles")
        else:
            # Crear una lista con las claves del diccionario para mostrarlas
            options = list(dictionary.keys())

            select = st.selectbox('Selecciona una opción:', options)

            if gui_controller_obj.get_sold(select) < gui_controller_obj.get_capacity(select):

                st.write('Nombre del evento:', select)

                # Selección de fase para saber el precio de la boleta
                sales_phase = st.radio("Fase de venta", ['Preventa', 'Venta regular'], index = 0, format_func = lambda x: x.upper())
                ticket_price = gui_controller_obj.get_ticket_price(select, sales_phase)
                st.write('Valor de la boleta: ', ticket_price)

                pay = st.radio("Método de pago", ['Tarjeta', 'Efectivo'], index = 0, format_func = lambda x: x.upper())

                first_name = st.text_input("Nombre comprador")
                last_name = st.text_input("Apellido comprador")
                user_id = st.text_input("ID del comprador")
                user_mail = st.text_input("Correo electronico")
                reason = st.text_input("Como se entero del evento")

                # Asignar valor de descuento
                discount = st.radio("Aplicar descuento", ['No', 'Si'], index = 0, format_func = lambda x: x.upper())

                discount_value = None
                if discount == 'Si':
                    discount_value = st.number_input("Porcentaje del descuento", step = 1)

                if st.session_state['event_type'] == "philanthropic_event":

                    if st.button("Registrar usuario", use_container_width = True):

                        ans = gui_controller_obj.new_user(first_name, last_name, user_id, user_mail, select, reason, 0)

                        if ans:
                            st.success("El usuario fue registrado exitosamente")
                        elif not ans:
                            st.warning("El usuario no fue registrado exitosamente")
                else:

                    if st.button("Comprar boleta", use_container_width = True):

                        if discount == 'Si':
                            ans = gui_controller_obj.new_user(first_name, last_name, user_id, user_mail, select, reason, discount_value, sales_phase, pay, ticket_price)
                        else:
                            ans = gui_controller_obj.new_user(first_name, last_name, user_id, user_mail, select, reason, 0, sales_phase, pay, ticket_price)

                        pdf_bytes = gui_controller_obj.create_pdf(select, first_name)
                        st.download_button(label = "Descargar PDF", data = pdf_bytes, file_name = "boleta.pdf", mime = "application/pdf")

                        if ans:
                            st.success("La boleta fue creada exitosamente")
                        elif not ans:
                            st.warning("La boleta no fue creada exitosamente")

            else:
                st.write("La capacidad del evento esta completa")
    else:
        st.write("No hay eventos creados")

    if st.button("Regresar", use_container_width = True):
        st.session_state['page'] = "show_view"
        st.rerun()


# Estructura de la pagina del bar
def bar_page(gui_controller_obj):

    st.markdown(BAR_TITLE_STYLE, unsafe_allow_html = True)

    # Inicializa un nuevo estado para saber que tipo de evento se esta creando y llamar al constructor
    st.session_state['event_type'] = 'bar_event'

    # Muestra todos los input donde se asigna la información
    input_info(gui_controller_obj)

    # Barra lateral con el resumen del evento que se esta creando
    with st.sidebar:
        st.write(" ")


# Estructura de la pagina del teatro
def theater_page(gui_controller_obj):

    st.markdown(THEATER_TITLE_STYLE, unsafe_allow_html = True)
    with st.sidebar:
        st.write(" ")

    st.session_state['event_type'] = 'theater_event'

    input_info(gui_controller_obj)


# Estructura evento filantropico
def philanthropic_page(gui_controller_obj):

    st.markdown(PHILANTHROPIC_TITLE_STYLE, unsafe_allow_html = True)
    with st.sidebar:
        st.write(" ")

    st.session_state['event_type'] = 'philanthropic_event'

    input_info(gui_controller_obj)


# Modifica los estados de los eventos y elimina
def modify_page(gui_controller_obj):

    st.session_state['page'] = "modify"

    st.markdown(TITLE_MODIFICATION, unsafe_allow_html = True)
    select_event = st.radio("Tipo de evento", ['Bar', 'Teatro', 'Filantropico'], index = 0, format_func = lambda x: x.upper())

    if 'dictionary' in st.session_state:
        # Imprime todas las opciones de evento que hay en el diccionario
        dictionary = {}
        if select_event == "Bar":
            st.session_state['event_type'] = "bar_event"
            dictionary = gui_controller_obj.get_dictionary("bar_record")
        elif select_event == "Teatro":
            st.session_state['event_type'] = "theater_event"
            dictionary = gui_controller_obj.get_dictionary("theater_record")
        elif select_event == "Filantropico":
            st.session_state['event_type'] = "philanthropic_event"
            dictionary = gui_controller_obj.get_dictionary("philanthropic_record")

        if not dictionary:
            st.write("No hay eventos disponibles")
        else:
            # Crear una lista con las claves del diccionario para mostrarlas
            options = list(dictionary.keys())

            select = st.selectbox('Selecciona una opción:', options)
            st.write('Nombre del evento:', select)

            # Seleccionar que tipo de modificación se le va a realizar al evento
            select_event = st.radio("Tipo de modificación", ['Modificar estado', 'Eliminar evento'], index = 0, format_func = lambda x: x.upper())
            # Obtiene el estado del evento
            event_status = gui_controller_obj.get_status(select)

            if select_event == "Modificar estado":

                # Verifica el estado del evento para saber si se puede realizar
                if event_status == "Realizado":
                    st.write("El evento ya ha sido realizado, no se puede modificar")
                else:

                    # Modifica el estado del evento
                    st.write("Seleccionar nuevo estado")
                    event_status = st.selectbox("Estado del evento", ["Realizado", "Por realizar", "Cancelado", "Aplazado", "Cerrado"])

                    if st.button("Modificar evento", use_container_width = True):
                        ans = gui_controller_obj.set_status(event_status, select)

                        if ans:
                            st.success("El estado fue modificado exitosamente")
                        else:
                            st.warning("El estado no fue modificado")

            else:

                if gui_controller_obj.get_sold(select) > 0:
                    st.warning('No se puede eliminar el evento, tiene boleteria vendida')
                else:

                    if st.button("Eliminar evento", use_container_width = True):
                        ans = gui_controller_obj.delete_event(select)

                        if ans:
                            st.success("El evento fue eliminado")
                        else:
                            st.warning("El evento no fue eliminado")

    else:
        st.write("No hay eventos disponibles")

    if st.button("Regresar", use_container_width = True):
        st.session_state['page'] = "show_view"
        st.rerun()


# Registra la asistencia de los usuarios al evento
def record_page(gui_controller_obj):

    st.markdown(REGISTRATION_TITLE, unsafe_allow_html = True)
    select_event = st.radio("Tipo de evento", ['Bar', 'Teatro', 'Filantropico'], index = 0, format_func = lambda x: x.upper())

    if 'dictionary' in st.session_state:

        # Imprime todas las opciones de evento que hay en el diccionario
        dictionary = {}
        if select_event == "Bar":
            st.session_state['event_type'] = "bar_event"
            dictionary = gui_controller_obj.get_dictionary("bar_record")
        elif select_event == "Teatro":
            st.session_state['event_type'] = "theater_event"
            dictionary = gui_controller_obj.get_dictionary("theater_record")
        elif select_event == "Filantropico":
            st.session_state['event_type'] = "philanthropic_event"
            dictionary = gui_controller_obj.get_dictionary("philanthropic_record")

        if not dictionary:
            st.write("No hay eventos disponibles")
        else:
            # Crear una lista con las claves del diccionario para mostrarlas
            options = list(dictionary.keys())

            select = st.selectbox('Selecciona una opción:', options)
            username = st.text_input("Nombre del usuario")

            if st.button("Marcar asistencia"):

                # Funcion que modifica la asistencia del usuario
                ans = gui_controller_obj.change_attendance(select, username)

                if ans:
                    st.success("El usuario fue registrado")
                else:
                    st.warning("El usuario no fue registrado")

    else:
        st.write("No hay eventos disponibles")

    if st.button("Regresar", use_container_width = True):
        st.session_state['page'] = "show_view"
        st.rerun()


# Generación de reportes
def report_page(gui_controller_obj):

    select_event = st.radio("Tipo de evento", ['Bar', 'Teatro', 'Filantropico'], index = 0, format_func = lambda x: x.upper())

    if 'dictionary' in st.session_state:
        dictionary = {}
        if select_event == "Bar":
            st.session_state['event_type'] = "bar_event"
            dictionary = gui_controller_obj.get_dictionary("bar_record")
        elif select_event == "Teatro":
            st.session_state['event_type'] = "theater_event"
            dictionary = gui_controller_obj.get_dictionary("theater_record")
        elif select_event == "Filantropico":
            st.session_state['event_type'] = "philanthropic_event"
            dictionary = gui_controller_obj.get_dictionary("philanthropic_record")

        if not dictionary:
            st.write("No hay eventos disponibles")
        else:

            st.title("Reportes")

            # Crear una lista con las claves del diccionario para mostrarlas
            options = list(dictionary.keys())
            event_name = st.selectbox('Selecciona una opción:', options)

            report_type = st.selectbox("Selecciona el tipo de reporte:", ["Reporte boletas", "Reporte financiero", "Reporte de compradores", "Graficas"])

            # Almacena la informacion en una sesion de estado para que no elimine al seleccionar una opcion
            if report_type == "Reporte boletas":

                st.session_state['event_data'] = {
                    'event_name': event_name,
                    'pre_sale_tickets': gui_controller_obj.get_pre_sale_ticket(event_name),
                    'regular_sales_tickets': gui_controller_obj.get_regular_sales_tickets(event_name),
                    'total_sold': gui_controller_obj.get_sold(event_name),
                    'ticket_price_preventa': gui_controller_obj.get_ticket_price(event_name, "Preventa"),
                    'ticket_price_regular': gui_controller_obj.get_ticket_price(event_name, "Venta regular"),
                    'cash_preventa': gui_controller_obj.get_cash(event_name, "Preventa"),
                    'card_preventa': gui_controller_obj.get_card(event_name, "Preventa"),
                    'cash_regular': gui_controller_obj.get_cash(event_name, "Venta regular"),
                    'card_regular': gui_controller_obj.get_card(event_name, "Venta regular"),
                    'users_dict': gui_controller_obj.get_dict_users(event_name),
                }

                # Muestra la informacion almacena en la sesion de estado
                if 'event_data' in st.session_state:
                    event_data = st.session_state['event_data']
                    st.write("Boletas de preventa: ", event_data['pre_sale_tickets'])
                    st.write("Boletas de venta regular: ", event_data['regular_sales_tickets'])
                    st.write("Boletas totales: ", event_data['total_sold'])

                    if st.session_state['event_type'] == "philanthropic_event":
                        st.write("Boletas de cortesia: ", event_data['total_sold'])
                    else:
                        val = 0
                        st.write("Boletas de cortesia: ", val)

                    if st.session_state['event_type'] != "philanthropic_event":
                        st.write("Ingresos totales preventa: ", event_data['ticket_price_preventa'] * event_data['pre_sale_tickets'])
                        st.write("Ingresos totales venta regular: ", event_data['ticket_price_regular'] * event_data['regular_sales_tickets'])

            elif report_type == "Reporte financiero":

                event_data = st.session_state['event_data']
                st.title("Reporte financiero")
                st.subheader("Boletería de preventa")
                st.write("Efectivo", event_data['cash_preventa'])
                st.write("Tarjeta", event_data['card_preventa'])

                st.subheader("Boletería de venta regular")
                st.write("Efectivo", event_data['cash_regular'])
                st.write("Tarjeta", event_data['card_regular'])

            elif report_type == "Reporte de compradores":

                event_data = st.session_state['event_data']
                st.title("Reporte de datos de los compradores")
                st.subheader("Información compradores")

                # Obtiene el diccionario con todos los objetos para poder acceder a la información
                dictionary_users = gui_controller_obj.get_dict_users(event_name)
                users = list(dictionary_users.keys())
                username = st.selectbox('Selecciona una opción:', users)

                # Mostrar información del usuario seleccionado
                user_info = event_data['users_dict'][username]
                st.write("Nombre: ", user_info.get_first_name())
                st.write("Apellido: ", user_info.get_last_name())
                st.write("Numero de indentificación: ", user_info.get_identification())
                st.write("Email: ", user_info.get_email())

            elif report_type == "Graficas":

                # Llama a la función graphics para obtener el gráfico con la informacion
                fig_sale, fig_pay, dfs, dfp = gui_controller_obj.graphics(event_name)

                # Muestra el gráfico
                st.plotly_chart(fig_sale)
                # Convierte el grafico a Excel
                excel_data_sale = gui_controller_obj.to_excel(dfs)
                col1, col2, col3 = st.columns(3)
                with col2:

                    # Boton para descargar la información
                    st.download_button(
                        label = "Excel tipos de pago",
                        data = excel_data_sale,
                        file_name = "data_sale.xlsx",
                        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width = True
                    )

                st.plotly_chart(fig_pay)
                excel_data_pay = gui_controller_obj.to_excel(dfp)

                col1, col2, col3 = st.columns(3)
                with col2:

                    st.download_button(
                        label = "Excel metodos de pago",
                        data = excel_data_pay,
                        file_name = "data_pay.xlsx",
                        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )

    else:
        st.write("No hay eventos disponibles")

    if st.button("Regresar", use_container_width = True):
        st.session_state['page'] = "show_view"
        st.rerun()


def report_by_artist(gui_controller_obj):

    st.title("Buscar evento por artista")
    art_name = st.text_input("Nombre del artista")

    if st.button("Buscar", use_container_width = True):

        event_name, event_type = gui_controller_obj.find_event(art_name)
        event_date, place, capacity = gui_controller_obj.get_info(event_name)

        ticket = gui_controller_obj.get_sold(event_name)

        percentage = (ticket / capacity) * 100

        st.session_state['event_type'] = event_type
        st.write("Nombre del evento: ", event_name)
        st.write("Fecha del evento: ", event_date)
        st.write("Lugar: ", place)
        st.write("Numero de boletas vendidas:", ticket)
        st.write("Porcentaje de aforo cubierto:", percentage)

    if st.button("Regresar", use_container_width=True):
        st.session_state['page'] = "show_view"
        st.rerun()


def dashboard(gui_controller_obj):

    st.title("Dashboard")
    if 'dictionary' in st.session_state:

        result = gui_controller_obj.update_count()

        # Convierte las tuplas en un DataFrame para separar los datos
        df = pd.DataFrame(result, columns = ['Date', 'Count'])
        df['Date'] = pd.to_datetime(df['Date'])  # Lo muestra en formato de fechas

        # Definir el rango de fechas, se establece como mínimo y maximo del DataFrame
        st.title('Evento por fechas')
        start_date = st.date_input('Fecha de inicio', df['Date'].min())
        end_date = st.date_input('Fecha de fin', df['Date'].max())

        # Filtramos el DataFrame según el rango de fechas ingresado
        filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

        # Crear la gráfica con tamaño personalizado
        fig, ax = plt.subplots(figsize = (8, 4))  # Tamaño en pulgadas (ancho, alto)
        ax.plot(filtered_df['Date'], filtered_df['Count'], marker = 'o', linestyle='-')
        ax.set_xlabel('Fecha', fontsize = 10)  # Tamaño de la fuente del eje x
        ax.set_ylabel('Eventos por fecha', fontsize = 10)  # Tamaño de la fuente del eje y
        ax.set_title('Eventos', fontsize = 12)  # Tamaño de la fuente del título

        # Ajustar el tamaño de la fuente de los ticks del eje x y eje y
        ax.tick_params(axis='x', labelsize = 8)
        ax.tick_params(axis='y', labelsize = 8)

        # Mostrar la gráfica en Streamlit
        st.pyplot(fig)

    else:
        st.write("No hay eventos creados")

    if st.button("Regresar", use_container_width=True):
        st.session_state['page'] = "show_view"
        st.rerun()
