# crate.py

class Crate:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.exists = True  # La caisse existe tant qu'elle n'est pas détruite
