from controllers.system_controller import SystemController
from models.artist import Artist
from models.bar import Bar
from models.philanthropic import Philanthropic
from models.theater import Theater
from models.ticket import Ticket
from models.user import User
import pytest


@pytest.fixture
def system_controller():
    return SystemController()


def test_singleton_system_controller():
    controller1 = SystemController()
    controller2 = SystemController()
    assert controller1 is controller2


def test_system_controller_dictionary_operations(system_controller):
    system_controller.set_dictionary("test_dict", {})
    assert system_controller.get_diccionario("test_dict") == {}
    system_controller.add_dictionary("test_dict", "key1", "value1")
    assert system_controller.get_diccionario("test_dict") == {"key1": "value1"}
    assert system_controller.size_diccionarios() == 1


def test_artist_methods():
    artist = Artist("John Doe", 1000, 2)
    assert artist.get_name() == "John Doe"
    assert artist.get_money() == 1000
    artist.set_utility(500)
    assert artist.get_artist_utility() == 500


def test_bar_event_methods():
    artist = Artist("John Doe", 1000, 2)
    bar_event = Bar("Bar Event", "2024-06-01", "18:00", "20:00", "Bar X",
                    "123 Main St", "City", "Active", 20.0, {1: artist}, 100)
    assert bar_event.get_ticket_price() == 20.0
    assert bar_event.get_tickets_sold() == 0
    bar_event.set_utility(1000)
    assert bar_event.utility == 1000


def test_philanthropic_event():
    artist = Artist("John Doe", 1000, 2)
    sponsors = ["Company A", "Company B"]
    philanthropic_event = Philanthropic("Event", "2024-06-01", "18:00", "20:00", "Place",
                                        "123 Main St", "City", "Active", {1: artist}, sponsors, 100)
    assert philanthropic_event.sponsors == sponsors


def test_theater_event_methods():
    artist = Artist("John Doe", 1000, 2)
    theater_event = Theater("Theater Event", "2024-06-01", "18:00", "20:00", "Theater X",
                            "123 Main St", "City", "Active", 50.0, {1: artist}, 200, 500)
    assert theater_event.get_ticket_price() == 50.0
    theater_event.set_utility(2000)
    assert theater_event.utility == 2000


def test_ticket_methods():
    ticket = Ticket("Alice", "Concert", 1)
    assert ticket.get_username() == "Alice"
    assert ticket.get_reason() == "Concert"
    assert ticket.get_capacity() == 1


def test_user_methods():
    user = User("Alice", "Smith", "123456", "alice@example.com", "I love music", False)
    assert user.get_first_name() == "Alice"
    assert user.get_last_name() == "Smith"
    assert user.get_identification() == "123456"
    assert user.get_email() == "alice@example.com"
    user.set_attendance(True)
    assert user.attendance == True
