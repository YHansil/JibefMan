# bomb.py

from constants import EXPLOSION_DELAY  # Ajoutez cette ligne pour importer la constante

class Bomb:
    def __init__(self, x, y, timer=EXPLOSION_DELAY):
        self.x = x
        self.y = y
        self.timer = timer  # Temps avant explosion
        self.exploded = False  # Indique si la bombe a explosé ou non

    def decrement_timer(self):
        """Décrémente le timer de la bombe."""
        if self.timer > 0:
            self.timer -= 1
        elif self.timer == 0:
            self.exploded = True  # La bombe explose une fois le timer à zéro
