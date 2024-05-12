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
