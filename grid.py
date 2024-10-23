from player import Player1, Player2

def print_grid(players, bombs, crates, explosion_zones):
    grid = [['.' for _ in range(10)] for _ in range(10)]  # Création de la grille

    for player in players:
        if player.alive:
            grid[player.y][player.x] = 'P' if isinstance(player, Player1) else 'E'

    for bomb in bombs:
        if not bomb.exploded:
            grid[bomb.y][bomb.x] = '0'  # Affiche la position de la bombe

    for crate in crates:
        if crate.exists:
            grid[crate.y][crate.x] = 'C'  # Affiche une caisse

    # Marquer les zones d'explosion
    for x, y in explosion_zones:
        grid[y][x] = 'X'  # Marque la zone d'explosion comme X

    for row in grid:
        print(' '.join(row))  # Affiche la grille
