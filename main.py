import pygame
import time
import random

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre et de la grille
GRID_SIZE = 10
CELL_SIZE = 50
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE #taille de la grille en largeur
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE #taille de la grille en hauteur

# Couleurs
WHITE = (255, 255, 255)
darkRED = (133, 6, 6)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Créer une fenêtre
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Bomberman")

# Position initiale du joueur (aligné à la grille)
player_x = 0
player_y = 0
player_size = CELL_SIZE

# Carte de la grille : 0 = libre, 1 = explosée, 2 = caisse
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Ajouter des caisses aléatoirement sur la grille avec une limite de 10 caisses
def ajout_caisses(num_caisses):
    count = 0
    while count < num_caisses :  # Limiter à 10 caisses maximum
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        # Vérifier que la case est vide et n'est pas la position initiale du joueur
        if grid[y][x] == 0 and not (x == player_x // CELL_SIZE and y == player_y // CELL_SIZE):
            grid[y][x] = 2  # 2 représente une caisse
            count += 1

# Ajouter 10 caisses aléatoirement au début
ajout_caisses(10)

# Liste pour stocker les bombes
bombs = []
game_over = False
game_win = False

# Classe pour représenter une bombe
class Bomb:
    def __init__(self, grid_x, grid_y):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.exploded = False
        self.time_planted = time.time()
        self.explosion_time = None  # Temps d'explosion (None tant qu'elle n'a pas explosé)
        self.color_reset_time = None  # Temps pour réinitialiser la couleur après explosion

    def update(self):
        global game_over
        current_time = time.time()

        # Bombe explose après 3 secondes
        if not self.exploded and current_time - self.time_planted >= 3:
            self.exploded = True
            self.explosion_time = current_time  # Marquer l'heure de l'explosion
            self.explode()

        # Si la bombe a explosé, garder la case rouge pendant 3 secondes
        if self.exploded and self.explosion_time is not None:
            if current_time - self.explosion_time >= 3:
                # Après 3 secondes, remettre la case en noir
                grid[self.grid_y][self.grid_x] = 0  # Case redevient noire
                self.color_reset_time = current_time  # Marquer le moment où la couleur est remise à noir

    def explode(self):
        global game_over
        # Marquer la case de la bombe comme explosée (rouge)
        grid[self.grid_y][self.grid_x] = 1

        # Vérifier si le joueur est sur la même case que la bombe au moment de l'explosion
        if self.grid_x == player_x // CELL_SIZE and self.grid_y == player_y // CELL_SIZE:
            game_over = True

        # Détruire les caisses autour (haut, bas, gauche, droite)
        self.destroy_box(self.grid_x - 1, self.grid_y)  # Gauche
        self.destroy_box(self.grid_x + 1, self.grid_y)  # Droite
        self.destroy_box(self.grid_x, self.grid_y - 1)  # Haut
        self.destroy_box(self.grid_x, self.grid_y + 1)  # Bas

    def destroy_box(self, grid_x, grid_y):
        if 0 <= grid_x < GRID_SIZE and 0 <= grid_y < GRID_SIZE:
            if grid[grid_y][grid_x] == 2:  # Si une caisse est présente
                grid[grid_y][grid_x] = 0  # Caisse détruite (la case redevient vide)

    def draw(self):
        # Dessiner la bombe seulement si elle n'a pas encore explosé
        if not self.exploded:
            pygame.draw.rect(screen, darkRED, (self.grid_x * CELL_SIZE, self.grid_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Ajouter une fonction pour vérifier si toutes les caisses ont été détruites
def check_win_condition():
    for row in grid:
        if 2 in row:  # S'il reste encore une caisse (2), retourner False
            return False
    return True

# Fonction pour réinitialiser le jeu
def reset_game():
    global player_x, player_y, bombs, grid, game_over, game_win
    player_x = 0
    player_y = 0
    bombs = []
    grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    ajout_caisses(10)  # Réinitialiser les caisses avec une limite de 10
    game_over = False
    game_win = False

# Fonction pour déposer une bombe
def drop_bomb(grid_x, grid_y):
    bomb = Bomb(grid_x, grid_y)
    bombs.append(bomb)

# Fonction pour dessiner le joueur
def draw_player(grid_x, grid_y):
    pygame.draw.rect(screen, GREEN, (grid_x * CELL_SIZE, grid_y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Fonction pour dessiner la grille, les explosions et les caisses
def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[y][x] == 1:  # Case explosée (rouge pendant l'explosion)
                pygame.draw.rect(screen, RED, rect)
            elif grid[y][x] == 2:  # Caisse
                pygame.draw.rect(screen, YELLOW, rect)
            # Dessiner la grille (optionnel)
            pygame.draw.rect(screen, WHITE, rect, 1)

# Fonction pour dessiner les bombes
def draw_bombs():
    for bomb in bombs:
        bomb.update()
        bomb.draw()

# Fonction pour afficher le message Game Over
def show_game_over():
    font = pygame.font.SysFont(None, 15)
    text = font.render("Game Over! cliquer sur R pour rejouer", True, RED)
    screen.blit(text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))

# Fonction pour afficher le message "Vous avez gagné"
def show_game_won():
    font = pygame.font.SysFont(None, 15)
    text = font.render("Vous avez gagné! cliquer sur R pour rejouer", True, GREEN)
    screen.blit(text, (SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2))

# Boucle de jeu
running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over and not game_win:
                # Déposer une bombe à la position actuelle du joueur
                if event.key == pygame.K_SPACE:
                    # Vérifier si le joueur peut déposer une bombe (pas sur une caisse)
                    grid_x = player_x // CELL_SIZE
                    grid_y = player_y // CELL_SIZE
                    if grid[grid_y][grid_x] != 2:  # Pas de caisse
                        drop_bomb(grid_x, grid_y)
                # Mouvements du joueur (basé sur la grille)
                if event.key == pygame.K_LEFT:
                    new_x = player_x - CELL_SIZE
                    if new_x >= 0 and grid[player_y // CELL_SIZE][new_x // CELL_SIZE] != 2:
                        player_x = new_x
                if event.key == pygame.K_RIGHT:
                    new_x = player_x + CELL_SIZE
                    if new_x < SCREEN_WIDTH and grid[player_y // CELL_SIZE][new_x // CELL_SIZE] != 2:
                        player_x = new_x
                if event.key == pygame.K_UP:
                    new_y = player_y - CELL_SIZE
                    if new_y >= 0 and grid[new_y // CELL_SIZE][player_x // CELL_SIZE] != 2:
                        player_y = new_y
                if event.key == pygame.K_DOWN:
                    new_y = player_y + CELL_SIZE
                    if new_y < SCREEN_HEIGHT and grid[new_y // CELL_SIZE][player_x // CELL_SIZE] != 2:
                        player_y = new_y
            # Recommencer le jeu si le joueur est mort ou a gagné
            if (game_over or game_win) and event.key == pygame.K_r:
                reset_game()

    # Dessiner la grille, les bombes et le joueur
    draw_grid()
    draw_bombs()  # Dessiner les bombes avant le joueur pour que le joueur apparaisse par-dessus les bombes

    if not game_over and not game_win:
        draw_player(player_x // CELL_SIZE, player_y // CELL_SIZE)

    # Vérification de la condition de victoire après chaque mise à jour de la bombe
    if check_win_condition():
        game_win = True

    # Afficher les messages correspondants
    if game_over:
        show_game_over()
    elif game_win:
        show_game_won()

    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
