from models.event import Event


# Controla toda la información del bar y hereda de Evento
class Bar(Event):

    # Declaración de los atributos con su respectiva herencia de la clase Evento
    def __init__(self, event_name, event_date, opening, show_time, place, address, city, event_status, ticket_price_pre_sale, ticket_regular, artist_info, capacity):
        super().__init__(event_name, event_date, opening, show_time, place, address, city, event_status, artist_info, capacity)

        self.ticket_price_pre_sale = ticket_price_pre_sale
        self.ticket_regular = ticket_regular
        self.utility = 0
        self.tickets_sold = 0
        self.total_cash_pre = 0
        self.total_cash_regular = 0
        self.total_card_pre = 0
        self.total_card_regular = 0

    def get_ticket_price(self, sales_phase):

        ans = 0
        if sales_phase == "Preventa":
            ans = self.ticket_price_pre_sale
        elif sales_phase == "Venta regular":
            ans = self.ticket_regular

        return ans

    def set_utility(self, utility):
        self.utility += utility

    def add_total_cash(self, total_cash, sales_phase):

        if sales_phase == "Preventa":
            self.total_cash_pre += total_cash
        else:
            self.total_cash_regular += total_cash

    def add_total_card(self, total_card, sales_phase):

        if sales_phase == "Preventa":
            self.total_card_pre += total_card
        else:
            self.total_card_regular += total_card

    def get_total_card(self, sales_phase):

        ans = None
        if sales_phase == "Preventa":
            ans = self.total_card_pre
        elif sales_phase == "Venta regular":
            ans = self.total_card_regular

        return ans

    def get_total_cash(self, sales_phase):

        ans = None
        if sales_phase == "Preventa":
            ans = self.total_cash_pre
        elif sales_phase == "Venta regular":
            ans = self.total_cash_regular

        return ans
