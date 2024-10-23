from bomb import Bomb
from crate import Crate
from player import Player1, Player2
from constants import GRID_SIZE, NUM_CRATES
import random
from grid import print_grid

def generate_crates(num_crates, players):
    crates = []
    while len(crates) < num_crates:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)

        if all((x, y) != (player.x, player.y) for player in players) and not any(c.x == x and c.y == y for c in crates):
            crates.append(Crate(x, y))  # Ajoute une nouvelle caisse
    return crates

def check_explosions(bombs, crates, players):
    explosion_zones = []  # Liste des zones d'explosion

    for bomb in bombs[:]:
        if bomb.turns_remaining == 0 and not bomb.exploded:
            bomb.explode()
            explosion_zones.append((bomb.x, bomb.y))

            # Zones adjacentes
            adjacent_positions = [(bomb.x, bomb.y),
                                  (bomb.x - 1, bomb.y),
                                  (bomb.x + 1, bomb.y),
                                  (bomb.x, bomb.y - 1),
                                  (bomb.x, bomb.y + 1)]

            for player in players:
                for pos in adjacent_positions:
                    if pos == (player.x, player.y):
                        player.alive = False  # Le joueur meurt s'il est sur la bombe ou dans la zone d'explosion

            for crate in crates:
                if (crate.x, crate.y) in adjacent_positions:
                    crate.exists = False  # La caisse est détruite

            bombs.remove(bomb)  # Supprime la bombe après l'explosion

        else:
            bomb.turns_remaining -= 1  # Diminue le nombre de tours restants

    return explosion_zones

def get_valid_spawn_position(players, crates):
    while True:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)

        if all((x, y) != (player.x, player.y) for player in players) and not any(c.x == x and c.y == y and c.exists for c in crates):
            return x, y  # Renvoie une position valide pour le spawn

def main():
    while True:  # Boucle pour rejouer
        players = [Player1(*get_valid_spawn_position([], []))]  # Premier joueur
        players.append(Player2(*get_valid_spawn_position(players, [])))  # Deuxième joueur

        crates = generate_crates(NUM_CRATES, players)  # Génère les caisses
        bombs = []  # Liste des bombes

        while all(player.alive for player in players):
            explosion_zones = []  # Réinitialise les zones d'explosion
            for player in players:
                if player.alive:
                    print_grid(players, bombs, crates, explosion_zones)

                    command = input(f"Joueur {'1' if player == players[0] else '2'} (Z, Q, S, D, E pour poser) : ").strip().lower()

                    new_x, new_y = player.x, player.y

                    if command == 'z' and player.y > 0:
                        new_y -= 1
                    elif command == 's' and player.y < GRID_SIZE - 1:
                        new_y += 1
                    elif command == 'q' and player.x > 0:
                        new_x -= 1
                    elif command == 'd' and player.x < GRID_SIZE - 1:
                        new_x += 1
                    elif command == 'e':
                        bombs.append(Bomb(player.x, player.y))  # Pose la bombe

                    # Vérifie les collisions avec les caisses et les autres joueurs
                    if not any(c.x == new_x and c.y == new_y and c.exists for c in crates) and \
                       all((new_x, new_y) != (other_player.x, other_player.y) for other_player in players if other_player != player):
                        player.x, player.y = new_x, new_y  # Déplace le joueur

            # Vérifie les explosions après que tous les joueurs aient joué
            explosion_zones = check_explosions(bombs, crates, players)

            # Marque les zones d'explosion pour la prochaine impression de la grille
            print_grid(players, bombs, crates, explosion_zones)

        # Affiche le message de victoire
        winner = players[0] if players[0].alive else players[1]
        print(f"Joueur {'1' if winner == players[0] else '2'} a gagné !")

        # Demande si les joueurs veulent rejouer
        replay = input("Voulez-vous rejouer ? (Y/N) : ").strip().upper()
        if replay != 'Y':
            break  # Quitte la boucle si les joueurs ne veulent pas rejouer

if __name__ == "__main__":
    main()
