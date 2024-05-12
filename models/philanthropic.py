from models.event import Event


class Philanthropic(Event):

    def __init__(self, event_name, event_date, opening, show_time, place, address, city, event_status, artist_info, sponsors):
        super().__init__(event_name, event_date, opening, show_time, place, address, city, event_status, artist_info)

        self.sponsors = sponsors
