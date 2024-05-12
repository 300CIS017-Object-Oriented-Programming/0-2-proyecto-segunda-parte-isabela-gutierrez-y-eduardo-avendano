class Ticket:

    def __init__(self, username, reason, capacity):
        self.username = username
        self.reason = reason
        self.capacity = capacity

    def get_username(self):
        return self.username

    def get_reason(self):
        return self.reason

    def get_capacity(self):
        return self.capacity

