class Ticket:

    def __init__(self, ticket_price_pre_sale, ticket_regular):
        self.ticket_price_pre_sale = ticket_price_pre_sale
        self.ticket_price_regular = ticket_regular
        self.total_pre_sale = 0
        self.total_regular = 0
        self.total_cash_pre = 0
        self.total_cash_regular = 0
        self.total_card_pre = 0
        self.total_card_regular = 0
        self.total_money = 0

    def get_ticket_price_pre_sale(self):
        return self.ticket_price_pre_sale

    def get_ticket_price_regular(self):
        return self.ticket_price_regular











    def get_total_pre_sale(self):
        return self.total_pre_sale

    def set_total_pre_sale(self, total_pre_sale):
        self.total_pre_sale += total_pre_sale














    def get_total_regular(self):
        return self.total_regular

    def set_total_regular(self, total_regular):
        self.total_regular += total_regular
















    def get_total_cash_pre(self):
        return self.total_cash_pre

    def set_total_cash_pre(self, total_cash_pre):
        self.total_cash_pre =+ total_cash_pre

    def get_total_cash_regular(self):
        return self.total_cash_regular

    def set_total_cash_regular(self, total_cash_regular):
        self.total_cash_regular += total_cash_regular

    def get_total_card_pre(self):
        return self.total_card_pre

    def set_total_card_pre(self, total_card_pre):
        self.total_card_pre += total_card_pre

    def get_total_card_regular(self):
        return self.total_card_regular

    def set_total_card_regular(self, total_card_regular):
        self.total_card_regular += total_card_regular

    def get_total_money(self):
        return self.total_money

    def set_total_money(self, total_money):
        self.total_money += total_money
