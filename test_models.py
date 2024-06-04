# Importa las funciones que necesitas para las pruebas
from models.artist import Artist
from models.bar import Bar
from models.event import Event
from models.philanthropic import Philanthropic
from models.theater import Theater
import pytest


# Pruebas unitarias para la clase Artist
def test_artist_class():

    artist_obj = Artist("Artista 1", "$100", "20:00")
    assert artist_obj.get_name() == "Artista 1"
    assert artist_obj.get_money() == "$100"


# Pruebas unitarias para la clase Bar
def test_bar_class():

    event_info = {
        "artist_info": {
            "artist_name": "Artista 1",
            "artist_price": "$100",
            "artist_time": "20:00"
        }
    }

    bar_obj = Bar("Evento Bar", "2024-05-30", "19:00", "21:00", "Bar XYZ", "Calle XYZ", "Ciudad XYZ", "Por realizar", "$50", event_info)
    assert bar_obj.get_event_name() == "Evento Bar"
    assert bar_obj.get_event_date() == "2024-05-30"
    assert bar_obj.get_opening() == "19:00"
    assert bar_obj.get_show_time() == "21:00"
    assert bar_obj.get_place() == "Bar XYZ"
    assert bar_obj.get_address() == "Calle XYZ"
    assert bar_obj.get_city() == "Ciudad XYZ"
    assert bar_obj.get_event_status() == "Por realizar"
    assert bar_obj.get_ticket_price() == "$50"
    assert bar_obj.get_artist_info() == event_info


# Pruebas unitarias para la clase Event
def test_event_class():
    event_obj = Event("Evento 1", "2024-05-29", "18:00", "20:00", "Lugar 1", "Calle 1", "Ciudad 1", "Realizado", {})
    assert event_obj.get_event_name() == "Evento 1"
    assert event_obj.get_event_date() == "2024-05-29"
    assert event_obj.get_opening() == "18:00"
    assert event_obj.get_show_time() == "20:00"
    assert event_obj.get_place() == "Lugar 1"
    assert event_obj.get_address() == "Calle 1"
    assert event_obj.get_city() == "Ciudad 1"
    assert event_obj.get_event_status() == "Realizado"


# Pruebas unitarias para la clase Philanthropic
def test_philanthropic_class():

    event_info = {
        "artist_info": {
            "artist_name": "Artista 1",
            "artist_price": "$100",
            "artist_time": "20:00"
        }
    }

    sponsors = {
        "Patrocinador 1": "$500",
        "Patrocinador 2": "$1000"
    }

    philanthropic_obj = Philanthropic("Evento Filantropico", "2024-06-15", "17:00", "19:00", "Lugar XYZ", "Calle XYZ", "Ciudad XYZ", "Por realizar", event_info, sponsors)
    assert philanthropic_obj.get_event_name() == "Evento Filantropico"
    assert philanthropic_obj.get_event_date() == "2024-06-15"
    assert philanthropic_obj.get_opening() == "17:00"
    assert philanthropic_obj.get_show_time() == "19:00"
    assert philanthropic_obj.get_place() == "Lugar XYZ"
    assert philanthropic_obj.get_address() == "Calle XYZ"
    assert philanthropic_obj.get_city() == "Ciudad XYZ"
    assert philanthropic_obj.get_event_status() == "Por realizar"
    assert philanthropic_obj.get_artist_info() == event_info
    assert philanthropic_obj.sponsors == sponsors


# Pruebas unitarias para la clase Theater
def test_theater_class():

    event_info = {
        "artist_info": {
            "artist_name": "Artista 1",
            "artist_price": "$100",
            "artist_time": "20:00"
        }
    }

    theater_obj = Theater("Evento Teatro", "2024-05-31", "18:00", "20:00", "Teatro XYZ", "Calle XYZ", "Ciudad XYZ", "Realizado", "$50", event_info, "$500")
    assert theater_obj.get_event_name() == "Evento Teatro"
    assert theater_obj.get_event_date() == "2024-05-31"
    assert theater_obj.get_opening() == "18:00"
    assert theater_obj.get_show_time() == "20:00"
    assert theater_obj.get_place() == "Teatro XYZ"
    assert theater_obj.get_address() == "Calle XYZ"
    assert theater_obj.get_city() == "Ciudad XYZ"
    assert theater_obj.get_event_status() == "Realizado"
    assert theater_obj.get_ticket_price() == "$50"
