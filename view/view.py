import streamlit as st
from settings import TITLE_STYLE, FOOTER, BAR_TITLE_STYLE, BUTTON_STYLE, TICKET_TITLE, THEATER_TITLE_STYLE, PHILANTHROPIC_TITLE_STYLE, TITLE_MODIFICATION
from datetime import date  # Muestra el calendario para el registro de fechas


def main_screen():

    col1, col2, col3 = st.columns(3)

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
        st.button("Otra cosa", use_container_width = True)

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
        capacity = st.text_input("Capacidad del evento")

    with col2:

        st.markdown("<h3 style = 'text-align: center'> Información artista </h3>", unsafe_allow_html = True)
        event_status = st.selectbox("Estado del evento", ["Realizado", "Por realizar", "Cancelado", "Aplazado", "Cerrado"])

        # Opcion para seleccionar la fases de venta (solo para teatro y bar)
        if st.session_state['event_type'] != "philanthropic_event":
            sales_phase = st.radio("Fase de venta", ['Preventa', 'Venta regular'], index = 0, format_func = lambda x: x.upper())

            if sales_phase == "Preventa":
                ticket_price = st.text_input("Valor de la boleta en preventa")
            else:
                ticket_price = st.text_input("Valor de la boleta regular")

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

            artist_obj_info = gui_controller_obj.create_artist(artist_name, artist_price, artist_time)
            artist_info[artist_name] = artist_obj_info

            artist_counter += 1

    # Llama al constructor de el evento bar si se encuentra en ese estado
    if st.session_state['event_type'] == "bar_event":

        if st.button("Crear evento Bar", use_container_width = True):

            # Se pasan los valores de los parametros para crear el objeto
            init_obj = gui_controller_obj.create_bar_event(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price, artist_info, capacity)

            # Informa al usuario si el evento se creo de manera exitosa
            if init_obj:
                st.success("Evento bar creado exitosamente")
            else:
                st.warning("Evento bar no creado exitosamente")

    if st.session_state['event_type'] == 'theater_event':

        theather_cost = st.text_input("Alquiler del teatro")

        if st.button("Crear evento teatro", use_container_width = True):

            init_obj = gui_controller_obj.create_theater_event(event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price, artist_info, theather_cost, capacity)

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


def buy_ticket(gui_controller_obj):

    st.session_state['page'] = "buy_ticket"

    st.markdown(TICKET_TITLE, unsafe_allow_html = True)
    select_event = st.radio("Tipo de evento", ['Bar', 'Teatro', 'Filantropico'], index = 0, format_func = lambda x: x.upper())

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

    options = []
    if not dictionary:
        st.write("No hay eventos disponibles")
    else:
        # Crear una lista con las claves del diccionario para mostrarlas
        options = list(dictionary.keys())

    select = st.selectbox('Selecciona una opción:', options)

    st.write('Nombre del evento:', select)

    first_name = st.text_input("Nombre comprador")
    last_name = st.text_input("Apellido comprador")
    user_id = st.text_input("ID del comprador")
    user_mail = st.text_input("Correo electronico")

    if st.session_state['event_type'] == "philanthropic_event":

        if st.button("Registrar usuario", use_container_width = True):
            ans = gui_controller_obj.new_user(first_name, last_name, user_id, user_mail, select)

            if ans:
                st.success("El usuario fue registrado exitosamente")
            elif not ans:
                st.warning("El usuario no fue registrado exitosamente")
    else:

        if st.button("Comprar boleta", use_container_width = True):
            ans = gui_controller_obj.new_user(first_name, last_name, user_id, user_mail, select)

            if ans:
                st.success("La boleta fue creada exitosamente")
            elif not ans:
                st.warning("La boleta no fue creada exitosamente")

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


def philanthropic_page(gui_controller_obj):

    st.markdown(PHILANTHROPIC_TITLE_STYLE, unsafe_allow_html = True)
    with st.sidebar:
        st.write(" ")

    st.session_state['event_type'] = 'philanthropic_event'

    input_info(gui_controller_obj)


def modify_page(gui_controller_obj):

    st.session_state['page'] = "modify"

    st.markdown(TITLE_MODIFICATION, unsafe_allow_html = True)
    select_event = st.radio("Tipo de evento", ['Bar', 'Teatro', 'Filantropico'], index = 0, format_func = lambda x: x.upper())

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

    options = []
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

    if st.button("Regresar", use_container_width = True):
        st.session_state['page'] = "show_view"
        st.rerun()
