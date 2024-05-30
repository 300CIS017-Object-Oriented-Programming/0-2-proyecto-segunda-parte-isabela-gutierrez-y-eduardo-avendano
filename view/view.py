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
        opening = st.time_input("Hora de apertura")
        show_time = st.time_input("Hora del evento")
        place = st.text_input("Lugar del evento")
        address = st.text_input("Dirección del evento")
        city = st.text_input("Ciudad del evento")
        capacity = st.number_input("Capacidad del evento", step = 1, min_value = 1)

    with col2:

        st.markdown("<h3 style = 'text-align: center'> Información artista </h3>", unsafe_allow_html = True)
        event_status = st.selectbox("Estado del evento", ["Por realizar", "Realizado", "Cancelado", "Aplazado", "Cerrado"])

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
            artist_price = st.number_input(f"Valor del contrato del artista {artist_counter + 1}", step = 1)
            artist_time = st.time_input(f"Hora de presentación del artista {artist_counter + 1}")

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

            ans = False
            if gui_controller_obj.get_status(select) == "Realizado":
                ans = True

            if gui_controller_obj.get_sold(select) < gui_controller_obj.get_capacity(select) and gui_controller_obj.get_status(select) != 'Realizado':

                st.write('Nombre del evento:', select)

                first_name = st.text_input("Nombre comprador")
                last_name = st.text_input("Apellido comprador")
                user_id = st.text_input("ID del comprador")
                user_mail = st.text_input("Correo electronico")
                reason = st.text_input("Como se entero del evento")

                if st.session_state['event_type'] == "philanthropic_event":

                    val = 0
                    st.write("Boleta de cortesia por un valor de: ", val)

                    if st.button("Registrar usuario", use_container_width = True):

                        ans = gui_controller_obj.new_user(first_name, last_name, user_id, user_mail, select, reason, "N/A", "N/A", 0)

                        if ans:
                            st.success("El usuario fue registrado exitosamente")
                        elif not ans:
                            st.warning("El usuario no fue registrado exitosamente")

                else:

                    # Selección de fase para saber el precio de la boleta
                    sales_phase = st.radio("Fase de venta", ['Preventa', 'Venta regular'], index=0, format_func=lambda x: x.upper())
                    ticket_price = gui_controller_obj.get_ticket_price(select, sales_phase)
                    st.write('Valor de la boleta: ', ticket_price)

                    payment_method = st.radio("Método de pago", ['Tarjeta', 'Efectivo'], index=0, format_func=lambda x: x.upper())

                    # Asignar valor de descuento
                    discount = st.radio("Aplicar descuento", ['No', 'Si'], index = 0, format_func = lambda x: x.upper())

                    if discount == 'Si':
                        # Pregunta el valor del descuento
                        discount_value = st.number_input("Porcentaje del descuento", step = 1)
                        ticket_price = ticket_price - (ticket_price * discount_value / 100)
                        st.write('Valor de la boleta con descuento: ', ticket_price)

                    if st.button("Comprar boleta", use_container_width = True):

                        # Crear el objeto con toda la información del usuario
                        ans = gui_controller_obj.new_user(first_name, last_name, user_id, user_mail, select, reason, sales_phase, payment_method, ticket_price)

                        pdf_bytes = gui_controller_obj.create_pdf(select, first_name)
                        st.download_button(label = "Descargar PDF", data = pdf_bytes, file_name = "boleta.pdf", mime = "application/pdf")

                        if ans:
                            st.success("La boleta fue creada exitosamente")
                        elif not ans:
                            st.warning("La boleta no fue creada exitosamente")

            else:

                if not ans:
                    st.write("La capacidad del evento esta completa")
                else:
                    st.write("El evento ya fue realizado")
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


# Estructura de la pagina filantropico
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

                # Muestra la informacion sobre las boletas vendidas
                st.write("Boletas de preventa: ", gui_controller_obj.get_pre_sale_ticket(event_name))
                st.write("Boletas de venta regular: ", gui_controller_obj.get_regular_sales_tickets(event_name))
                st.write("Boletas totales: ", gui_controller_obj.get_sold(event_name))

                if st.session_state['event_type'] == "philanthropic_event":
                    st.write("Boletas de cortesia: ", gui_controller_obj.get_sold(event_name))
                else:
                    st.write("Boletas de cortesia: ", 0)

                if st.session_state['event_type'] != "philanthropic_event":
                    st.write("Ingresos totales preventa: ", gui_controller_obj.get_total_phase("Preventa", event_name))
                    st.write("Ingresos totales venta regular: ", gui_controller_obj.get_total_phase("Venta regular", event_name))

            elif report_type == "Reporte financiero":

                st.title("Reporte financiero")
                st.subheader("Boletería de preventa")
                st.write("Efectivo", gui_controller_obj.get_cash(event_name, "Preventa"))
                st.write("Tarjeta", gui_controller_obj.get_card(event_name, "Preventa"))

                st.subheader("Boletería de venta regular")
                st.write("Efectivo", gui_controller_obj.get_cash(event_name, "Venta regular"))
                st.write("Tarjeta", gui_controller_obj.get_card(event_name, "Venta regular"))

            elif report_type == "Reporte de compradores":

                st.title("Reporte de datos de los compradores")
                st.subheader("Información compradores")

                # Obtiene el diccionario con todos los objetos para poder acceder a la información
                dictionary_users = gui_controller_obj.get_dict_users(event_name)
                users = list(dictionary_users.keys())
                username = st.selectbox('Selecciona una opción:', users)

                # Asigna el valor del diccionario a una variable
                user_info = dictionary_users[username]

                # Obtiene la informacion de los usuarios
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


# Permite buscar un evento por medio del artista
def report_by_artist(gui_controller_obj):
    st.title("Buscar evento por artista")
    art_name = st.text_input("Nombre del artista")

    if st.button("Buscar", use_container_width = True):
        event_name, event_type = gui_controller_obj.find_event(art_name)
        event_date, place, capacity = gui_controller_obj.get_info(event_name)
        ticket = gui_controller_obj.get_sold(event_name)

        # Asigna el tipo de evento dependiendo del diccionario donde esta almacenado
        if event_type == "bar_record":
            event_type = "bar_event"
        elif event_type == "theater_record":
            event_type = "theater_event"
        elif event_type == "philanthropic_record":
            event_type = "philanthropic_event"

        if capacity == 0:
            percentage = 0
        else:
            percentage = (ticket / capacity) * 100

        st.session_state['event_type'] = event_type

        st.write("Nombre del evento: ", event_name)
        st.write("Fecha del evento: ", event_date)
        st.write("Lugar: ", place)
        st.write("Numero de boletas vendidas:", ticket)
        st.write("Porcentaje de aforo cubierto:", percentage)

    if st.button("Regresar", use_container_width = True):
        st.session_state['page'] = "show_view"
        st.rerun()


# Crea la tabla de registros con sus graficas
def dashboard(gui_controller_obj):
    st.title("Dashboard de Gestión de Eventos")

    if 'dictionary' in st.session_state:
        # Obtener los datos de eventos
        result = gui_controller_obj.update_count()

        # Verificar los datos devueltos
        if len(result) == 0:
            st.write("No se encontraron eventos.")
            return

        # Asegurar que los datos tienen la estructura correcta
        if len(result[0]) == 5:
            df = pd.DataFrame(result, columns=['Date', 'Count', 'Event Type', 'Event Name', 'Total Money'])
        else:
            st.write("Formato de datos inesperado devuelto por update_count")
            return

        df['Date'] = pd.to_datetime(df['Date'])  # Convertir a formato de fecha

        # Definir el rango de fechas
        st.title('Eventos por Fechas')
        start_date = st.date_input('Fecha de inicio', df['Date'].min())
        end_date = st.date_input('Fecha de fin', df['Date'].max())

        # Filtrar el DataFrame según el rango de fechas
        filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]

        # Gráfico de cantidad de eventos por tipo
        event_type_count = filtered_df['Event Type'].value_counts()
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        ax1.bar(event_type_count.index, event_type_count.values)
        ax1.set_xlabel('Tipo de Evento', fontsize=10)
        ax1.set_ylabel('Cantidad de Eventos', fontsize=10)
        ax1.set_title('Cantidad de Eventos por Tipo', fontsize=12)
        st.pyplot(fig1)

        # Mostrar la gráfica de eventos por fecha
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.plot(filtered_df['Date'], filtered_df['Count'], marker='o', linestyle='-')
        ax2.set_xlabel('Fecha', fontsize=10)
        ax2.set_ylabel('Eventos por fecha', fontsize=10)
        ax2.set_title('Eventos', fontsize=12)
        st.pyplot(fig2)

        # Mostrar tabla con los datos filtrados
        st.write("Datos de eventos en el rango de fechas seleccionado:")
        st.dataframe(filtered_df)

    else:
        st.write("No hay eventos creados")

    if st.button("Regresar", use_container_width=True):
        st.session_state['page'] = "show_view"
        st.rerun()


# Registra asistencia para hacer la tabla de registros
def register_attendance(gui_controller_obj):

    st.title("Gestión de Ingreso al Evento")

    # Supongamos que get_ticket_data devuelve una lista de tuplas con (ticket_id, buyer_name, event_name)
    ticket_data = gui_controller_obj.get_ticket_data()
    ticket_df = pd.DataFrame(ticket_data, columns = ['ticket id', 'buyer name', 'event name'])

    # Búsqueda de boletas vendidas o comprador
    search_term = st.text_input("Buscar por nombre del comprador o ID de la boleta")

    if st.button("Buscar"):
        if search_term.isdigit():
            result_df = ticket_df[ticket_df['ticket id'] == int(search_term)]
        else:
            result_df = ticket_df[ticket_df['buyer name'].str.contains(search_term, case = False)]

        if result_df.empty:
            st.write("No se encontraron resultados.")
        else:
            st.write("Resultados de la búsqueda:")
            st.dataframe(result_df)

            if st.button("Registrar Asistencia"):
                # Lógica para registrar la asistencia (esto puede implicar actualizar una base de datos)
                gui_controller_obj.register_attendance(result_df['ticket id'].values[0])
                st.write("Asistencia registrada para la boleta/comprador seleccionado.")
