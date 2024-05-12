import streamlit as st


# Almacena la información privada de cada evento
class SystemController:

    # Verifica que solo se cree una instancia de la clase para un manejo más sencillo (Singleton)
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__initialized = False
        return cls._instance

    # Definición de los atributos de la clase
    def __init__(self):
        self.__initialized = True

    # Crea dentro del estado los diccionarios con la información
    @staticmethod
    def set_dictionary(dict_name, dictionary):
        st.session_state['dictionary'][dict_name] = dictionary

    # Retorna el diccionario, dependiendo del nombre que se ingrese
    @staticmethod
    def get_diccionario(dict_name):
        return st.session_state['dictionary'].get(dict_name)

    # Añadir un nuevo valor al diccionario
    @staticmethod
    def add_dictionary(dict_name, key, value):
        st.session_state['dictionary'][dict_name][key] = value

    @staticmethod
    def size_diccionarios():
        diccionario = SystemController.get_diccionario('bar_record')
        if diccionario:
            ans = len(diccionario)
        else:
            ans = None

        return ans