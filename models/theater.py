from models.event import Event


class Theater(Event):

    def __init__(self, event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price, artist_info):
        super().__init__(event_name, event_date, opening, show_time, place, address, city, event_status, artist_info)

        self.ticket_price = ticket_price
