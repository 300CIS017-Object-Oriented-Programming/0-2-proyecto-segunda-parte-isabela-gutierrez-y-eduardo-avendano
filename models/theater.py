from models.event import Event


class Theater(Event):

    def __init__(self, event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price, artist_info, theater_rental):
        super().__init__(event_name, event_date, opening, show_time, place, address, city, event_status, artist_info)

        self.theater_rental = theater_rental
        self.ticket_price = ticket_price
        self.final_ticket_price = ticket_price
        self.ticket_sold = 0

    def get_ticket_price(self):
        return self.ticket_price
