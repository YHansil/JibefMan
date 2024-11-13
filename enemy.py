# enemy.py

import random
from bomb import Bomb
from constants import GRID_SIZE

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True

    def move(self, players):
        # Mouvement aléatoire pour l'ennemi
        direction = random.choice(['up', 'down', 'left', 'right'])
        new_x, new_y = self.x, self.y

        if direction == 'up' and self.y > 0:
            new_y -= 1
        elif direction == 'down' and self.y < GRID_SIZE - 1:
            new_y += 1
        elif direction == 'left' and self.x > 0:
            new_x -= 1
        elif direction == 'right' and self.x < GRID_SIZE - 1:
            new_x += 1

        # Vérifier si le mouvement n'entre pas en collision avec un joueur
        if not any(p.x == new_x and p.y == new_y for p in players):
            self.x, self.y = new_x, new_y

    def place_bomb(self, bombs):
        # Ne pas placer de bombe si l'ennemi est sur un joueur
        if self.alive:
            bombs.append(Bomb(self.x, self.y))
