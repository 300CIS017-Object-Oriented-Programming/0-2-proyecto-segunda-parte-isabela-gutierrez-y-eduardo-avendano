class Event:

    # Declaración de los atributos generales para que las demas clases utilicen
    def __init__(self, event_name, event_date, opening, show_time, place, address, city, event_status, artist_info, capacity):
        self.event_name = event_name
        self.event_date = event_date
        self.opening = opening
        self.show_time = show_time
        self.place = place
        self.address = address
        self.city = city
        self.event_status = event_status
        self.artist_info = artist_info
        self.tickets_sold = 0
        self.users = {}
        self.capacity = capacity
        self.pre_sale_tickets = 0
        self.regular_sales_tickets = 0

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

    def set_users(self, user_name, user_obj):
        self.users[user_name] = user_obj

    def add_ticket(self, sales_phase):

        if sales_phase == "Preventa":
            self.pre_sale_tickets += 1
        elif sales_phase == "Venta regular":
            self.regular_sales_tickets += 1

        self.tickets_sold += 1

    def get_status(self):
        return self.event_status

    def set_status(self, status):
        self.event_status = status

    def get_tickets_sold(self):
        return self.tickets_sold

    def get_capacity(self):
        return self.capacity

    def get_users(self):
        return self.users

    def add_pre_sale_ticket(self):
        self.pre_sale_tickets += 1

    def add_regular_sales_ticket(self):
        self.regular_sales_tickets += 1

    def get_regular_sales_tickets(self):
        return self.regular_sales_tickets

    def get_pre_sale_tickets(self):
        return self.pre_sale_tickets
