from models.event import Event


# Controla toda la información del bar y hereda de Evento
class Bar(Event):

    # Declaración de los atributos con su respectiva herencia de la clase Evento
    def __init__(self, event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price, artist_info):
        super().__init__(event_name, event_date, opening, show_time, place, address, city, event_status, artist_info)

        self.ticket_price = ticket_price
        self.money_event = 0
        self.tickets_sold = 0

    def get_ticket_price(self):
        return self.ticket_price
