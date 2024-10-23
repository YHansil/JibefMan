class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.turns_remaining = 3  # Délai réduit à 3 tours avant l'explosion
        self.exploded = False  # Indique si la bombe a explosé

    def explode(self):
        self.exploded = True
        print(f"Bombe explosée à la position ({self.x}, {self.y})")
