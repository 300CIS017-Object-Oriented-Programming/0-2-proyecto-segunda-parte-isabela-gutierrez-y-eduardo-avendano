class Artist:

    # Declaración de los atributos de la clase
    def __init__(self, artist_name, artist_money, artist_hour):
        self.name = artist_name
        self.money = artist_money
        self.time = artist_hour
        self.artist_utility = 0

    # Obtener el valor del nombre
    def get_name(self):
        return self.name

    # Obtener el dinero del artista
    def get_money(self):
        return self.money

    def set_utility(self, utility):
        self.artist_utility = utility

    def get_artist_utility(self):
        return self.artist_utility
