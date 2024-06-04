class User:

    def __init__(self, first_name, last_name, identification, email, reason, attendance, payment_method, ticket_price, sale_phase):
        self.first_name = first_name
        self.last_name = last_name
        self.identification = identification
        self.email = email
        self.reason = reason
        self.attendance = attendance
        self.user_ticket_price = ticket_price
        self.payment_method = payment_method
        self.sale_phase = sale_phase

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_identification(self):
        return self.identification

    def get_email(self):
        return self.email

    def set_attendance(self, attendance):
        self.attendance = attendance

    def get_sale_phase(self):
        return self.sale_phase

    def get_payment_method(self):
        return self.payment_method

    def get_ticket_price(self):
        return self.user_ticket_price
