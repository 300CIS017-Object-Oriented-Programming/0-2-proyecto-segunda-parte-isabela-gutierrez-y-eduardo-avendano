from models.event import Event


class Theater(Event):

    def __init__(self, event_name, event_date, opening, show_time, place, address, city, event_status, artist_info, theater_rental, capacity, ticket_info):
        super().__init__(event_name, event_date, opening, show_time, place, address, city, event_status, artist_info, capacity)

        self.theater_rental = theater_rental
        self.utility = 0
        self.ticket_info = ticket_info

    def get_ticket_price(self, sales_phase):

        ans = 0
        if sales_phase == "Preventa":
            ans = self.ticket_info.get_ticket_price_pre_sale()
        elif sales_phase == "Venta regular":
            ans = self.ticket_info.get_ticket_price_regular()

        return ans

    def set_utility(self, utility):
        self.utility = utility

    def add_total_cash(self, total_cash, sales_phase):

        if sales_phase == "Preventa":
            self.ticket_info.set_total_cash_pre(total_cash)
        else:
            self.ticket_info.set_total_cash_regular(total_cash)

    def add_total_card(self, total_card, sales_phase):

        if sales_phase == "Preventa":
            self.ticket_info.set_total_card_pre(total_card)
        else:
            self.ticket_info.set_total_card_regular(total_card)

    def get_total_card(self, sales_phase):

        ans = None
        if sales_phase == "Preventa":
            ans = self.ticket_info.get_total_card_pre()
        elif sales_phase == "Venta regular":
            ans = self.ticket_info.get_total_card_regular()

        return ans

    def get_total_cash(self, sales_phase):

        ans = None
        if sales_phase == "Preventa":
            ans = self.ticket_info.get_total_cash_pre()
        elif sales_phase == "Venta regular":
            ans = self.ticket_info.get_total_cash_regular()

        return ans

    def set_total_money(self, total_cash):
        self.ticket_info.set_total_money(total_cash)

    def get_total_money(self):
        return self.ticket_info.get_total_money()
