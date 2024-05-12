class Event:

    # Declaración de los atributos generales para que las demas clases utilicen
    def __init__(self, event_name, event_date, opening, show_time, place, address, city, event_status, artist_info):
        self.event_name = event_name
        self.event_date = event_date
        self.opening = opening
        self.show_time = show_time
        self.place = place
        self.address = address
        self.city = city
        self.event_status = event_status
        self.artist_info = artist_info

    # Set y Get para asignar y acceder a los atributos
    def get_event_name(self):
        return self.event_name

    def get_event_date(self):
        return self.event_date

    def get_opening(self):
        return self.opening

    def get_show_time(self):
        return self.show_time

    def get_place(self):
        return self.place

    def get_address(self):
        return self.address

    def get_city(self):
        return self.city

    def get_event_status(self):
        return self.event_status

    def get_artist_info(self):
        return self.artist_info
