# game.py

import random
from bomb import Bomb
from crate import Crate
from player import Player1, Player2
from constants import GRID_SIZE, NUM_CRATES, EXPLOSION_DELAY
from grid import print_grid, initialize_grid


def generate_crates(num_crates, players, grid):
    crates = []
    grid_height = len(grid)         # Hauteur de la grille
    grid_width = len(grid[0])       # Largeur de la grille

    while len(crates) < num_crates:
        x = random.randint(0, grid_width - 1)
        y = random.randint(0, grid_height - 1)

        if (
            grid[y][x] == ' ' and
            all((x, y) != (player.x, player.y) for player in players)
        ):
            crates.append(Crate(x, y))
            grid[y][x] = 'C'  # Marque la caisse sur la grille
    return crates


def check_explosions(bombs, crates, grid):
    explosion_zones = []  # Zones où l'explosion se produit
    for bomb in bombs[:]:
        bomb.decrement_timer()  # Décrémente le timer de chaque bombe
        if bomb.exploded:  # Si la bombe a explosé, on la traite
            # Définir les directions d'explosion (haut, bas, gauche, droite)
            x, y = bomb.x, bomb.y
            destroyed_crates = []  # Liste pour stocker les caisses détruites durant l'explosion

            # Explosion en haut
            if y > 0:  # Vérifie si on ne dépasse pas les bords de la grille
                explosion_zones.append((x, y - 1))
                for crate in crates:
                    if crate.x == x and crate.y == y - 1:
                        crate.exists = False  # Détruire la caisse
                        destroyed_crates.append(crate)

            # Explosion en bas
            if y < len(grid) - 1:  # Vérifie si on ne dépasse pas les bords de la grille
                explosion_zones.append((x, y + 1))
                for crate in crates:
                    if crate.x == x and crate.y == y + 1:
                        crate.exists = False  # Détruire la caisse
                        destroyed_crates.append(crate)

            # Explosion à gauche
            if x > 0:  # Vérifie si on ne dépasse pas les bords de la grille
                explosion_zones.append((x - 1, y))
                for crate in crates:
                    if crate.x == x - 1 and crate.y == y:
                        crate.exists = False  # Détruire la caisse
                        destroyed_crates.append(crate)

            # Explosion à droite
            if x < len(grid[0]) - 1:  # Vérifie si on ne dépasse pas les bords de la grille
                explosion_zones.append((x + 1, y))
                for crate in crates:
                    if crate.x == x + 1 and crate.y == y:
                        crate.exists = False  # Détruire la caisse
                        destroyed_crates.append(crate)

            # Marque la bombe comme ayant explosé
            bomb.exploded = True
            bombs.remove(bomb)  # Supprime la bombe de la liste après l'explosion

    return explosion_zones


def get_valid_spawn_position(players, crates, grid):
    while True:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)

        if (
            grid[y][x] == ' ' and
            all((x, y) != (player.x, player.y) for player in players) and
            not any(c.x == x and c.y == y and c.exists for c in crates)
        ):
            return x, y


def handle_player_action(player, command, bombs, grid, crates, players):
    new_x, new_y = player.x, player.y

    if player == players[0]:  # Joueur 1 est "P"
        if command == 'z' and player.y > 0:
            new_y -= 1
        elif command == 's' and player.y < len(grid) - 1:
            new_y += 1
        elif command == 'q' and player.x > 0:
            new_x -= 1
        elif command == 'd' and player.x < len(grid[0]) - 1:
            new_x += 1
        elif command == 'e':  # Commande pour poser une bombe
            bombs.append(Bomb(player.x, player.y))  # Pose la bombe
    elif player == players[1]:  # Joueur 2 est "E"
        if command == 'i' and player.y > 0:
            new_y -= 1
        elif command == 'k' and player.y < len(grid) - 1:
            new_y += 1
        elif command == 'j' and player.x > 0:
            new_x -= 1
        elif command == 'l' and player.x < len(grid[0]) - 1:
            new_x += 1
        elif command == 'o':  # Commande pour poser une bombe
            bombs.append(Bomb(player.x, player.y))  # Pose la bombe

    # Vérifie si la nouvelle position est valide
    if (
        grid[new_y][new_x] == ' ' and
        not any(c.x == new_x and c.y == new_y and c.exists for c in crates) and
        all((new_x, new_y) != (other_player.x, other_player.y) for other_player in players if other_player != player)
    ):
        player.x, player.y = new_x, new_y


def handle_explosions(explosion_zones, players):
    for player in players:
        if (player.x, player.y) in explosion_zones:
            player.alive = False  # Le joueur est tué si il est dans une zone d'explosion


def main():
    while True:
        grid = initialize_grid()  # Initialise la grille
        players = [Player1(*get_valid_spawn_position([], [], grid))]  # Spawn du premier joueur (P)
        players.append(Player2(*get_valid_spawn_position(players, [], grid)))  # Spawn du deuxième joueur (E)

        crates = generate_crates(NUM_CRATES, players, grid)  # Génère les caisses
        bombs = []  # Liste des bombes

        while all(player.alive for player in players):
            explosion_zones = []  # Réinitialise les zones d'explosion

            # Tour du Joueur 1 (P)
            print_grid(players, bombs, crates, explosion_zones, grid)
            command_p = input("Joueur P - Z/Q/S/D pour bouger, E pour poser une bombe : ").strip().lower()
            handle_player_action(players[0], command_p, bombs, grid, crates, players)

            # Vérifie les explosions après le tour du Joueur 1
            explosion_zones = check_explosions(bombs, crates, grid)
            handle_explosions(explosion_zones, players)  # Vérifie si un joueur est tué
            print_grid(players, bombs, crates, explosion_zones, grid)

            # Tour du Joueur 2 (E)
            print_grid(players, bombs, crates, explosion_zones, grid)
            command_e = input("Joueur E - I/J/K/L pour bouger, O pour poser une bombe : ").strip().lower()
            handle_player_action(players[1], command_e, bombs, grid, crates, players)

            # Vérifie les explosions après le tour du Joueur 2
            explosion_zones = check_explosions(bombs, crates, grid)
            handle_explosions(explosion_zones, players)  # Vérifie si un joueur est tué
            print_grid(players, bombs, crates, explosion_zones, grid)

            # Ajoute une ligne de séparation entre les tours
            print("\n" + "-" * 20 + "\n")

        # Affiche le message de victoire
        winner = players[0] if players[0].alive else players[1]
        print(f"Joueur {'P' if winner == players[0] else 'E'} a gagné !")

        # Demande si les joueurs veulent rejouer
        replay = input("Voulez-vous rejouer ? (Y/N) : ").strip().upper()
        if replay != 'Y':
            break  # Quitte la boucle si les joueurs ne veulent pas rejouer



if __name__ == "__main__":
    main()
