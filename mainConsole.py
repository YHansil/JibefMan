def initialiser_plateau():
    return [
        ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
        ['|', ' ', 'I', 'C', ' ', 'I', ' ', 'C', '|'],
        ['|', 'Y', ' ', 'C', ' ', ' ', ' ', 'I', '|'],
        ['|', 'I', ' ', 'E', ' ', 'I', ' ', ' ', '|'],
        ['|', ' ', 'I', ' ', ' ', 'E', 'C', ' ', '|'],
        ['|', 'E', 'C', ' ', 'I', ' ', ' ', ' ', '|'],
        ['|', ' ', 'I', ' ', ' ', 'E', 'C', ' ', '|'],
        ['|', ' ', 'I', 'C', ' ', ' ', ' ', 'C', '|'],
        ['-', '-', '-', '-', '-', '-', '-', '-', '-'],
    ]


# foction permettant d'afficher le plateau de jeu de manière correct 
def afficher_plateau(plateau):
    for ligne in plateau:
        print(' '.join(ligne))

def trouver_position(plateau, caractere):
    for i, ligne in enumerate(plateau):
        if caractere in ligne:
            return i, ligne.index(caractere)
    return None

def deplacer_joueur(plateau, direction):
    # Trouver la position actuelle du joueur ('Y')
    joueur_pos = trouver_position(plateau, 'Y')
    if joueur_pos is None:
        return plateau  # Si aucun joueur trouvé, ne rien faire

    x, y = joueur_pos
    nouvelle_position = None

    # Déterminer la nouvelle position selon la direction
    if direction == 'z' and x > 0:  # Haut
        nouvelle_position = (x - 1, y)
    elif direction == 's' and x < len(plateau) - 1:  # Bas
        nouvelle_position = (x + 1, y)
    elif direction == 'q' and y > 0:  # Gauche
        nouvelle_position = (x, y - 1)
    elif direction == 'd' and y < len(plateau[0]) - 1:  # Droite
        nouvelle_position = (x, y + 1)

    # Vérifier la nouvelle position
    if nouvelle_position:
        nx, ny = nouvelle_position
        if plateau[nx][ny] == 'E':  # Si la nouvelle case est occupée par un ennemi
            print("Vous avez rencontré un ennemi ! Défaite.")
            return None  # Le jeu s'arrête ici
        elif plateau[nx][ny] == ' ':  # Si la case est vide
            plateau[x][y] = ' '  # Ancienne position devient vide
            plateau[nx][ny] = 'Y'  # Nouvelle position devient celle du joueur

    return plateau

# Initialisation du plateau et affichage initial
plateau = initialiser_plateau()
afficher_plateau(plateau)

# Boucle principale pour les déplacements
while plateau is not None:
    direction = input("Déplacer le joueur (z=haut, q=gauche, s=bas, d=droite, x=quitter) : ")
    if direction == 'x':
        print("Fin du jeu")
        break
    plateau = deplacer_joueur(plateau, direction)
    if plateau is not None:
        afficher_plateau(plateau)
