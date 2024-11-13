from player import Player1, Player2

# grid.py

from constants import GRID_SIZE

def initialize_grid():
    # Crée une grille de taille GRID_SIZE x GRID_SIZE avec des murs autour
    grid = [[' ' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # Ajouter des murs autour de la grille
    for i in range(GRID_SIZE):
        grid[0][i] = '-'       # Mur en haut
        grid[GRID_SIZE - 1][i] = '-'  # Mur en bas
        grid[i][0] = '|'       # Mur à gauche
        grid[i][GRID_SIZE - 1] = '|'  # Mur à droite

    # Ajout de quelques obstacles (comme dans votre configuration initiale)
    # Cela peut être personnalisé pour ajouter des caisses ou autres obstacles
    return grid

# main.py ou game.py (selon où vous avez votre fonction `print_grid`)

def print_grid(players, bombs, crates, explosion_zones, grid):
    grid_copy = [row[:] for row in grid]  # Copie de la grille pour ne pas la modifier directement
    
    # Marque les joueurs avec 'P' et 'E'
    for i, player in enumerate(players):
        grid_copy[player.y][player.x] = 'P' if i == 0 else 'E'  # 'P' pour le joueur 1, 'E' pour le joueur 2
    
    # Marque les bombes
    for bomb in bombs:
        if bomb.exploded:
            grid_copy[bomb.y][bomb.x] = 'X'  # Marque une explosion par 'X'
        else:
            grid_copy[bomb.y][bomb.x] = 'B'  # Marque une bombe par 'B'

    # Marque les caisses
    for crate in crates:
        if crate.exists:
            grid_copy[crate.y][crate.x] = 'C'  # Marque une caisse par 'C'
        else:
            grid_copy[crate.y][crate.x] = ' '  # Enlève la caisse détruite
    
    # Marque les zones d'explosion
    for (ex_x, ex_y) in explosion_zones:
        grid_copy[ex_y][ex_x] = '*'  # Marque une zone d'explosion par '*'
    
    # Affichage de la grille
    for row in grid_copy:
        print(' '.join(row))


