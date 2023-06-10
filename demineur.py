"""
Titre : Projet d'année n°1, Démineur.
Prénom : Jawad
Nom : Cherkaoui 
Matricule : 576517
Entrées : La dimension du plateau de jeu ( 'n' lignes, 'm' colonnes) et le nombre de mines (number_of_mines).
Sortie : Affichage du jeu démineur dans le terminal.
But : L’objectif du projet est de réaliser une implémentation en Python 3 du Démineur. 
      C’est un jeu à 1 joueur sur une grille de taille variable et dont certaines cases contiennent des mines. 
      Le but du jeu est de dévoiler petit-à-petit les cases vides de la grille jusqu’à localiser toutes les mines et les “désamorcer”.
      Le joueur perd s’il dévoile une case contenant une mine.
"""

##############  À LIRE ATTENTIVEMENT  ##############
# Ce fichier python contient du code ANSI pour les couleurs, il peut donc être source de problème sous certain os !
# Il doit également être exécuté sous python 3.10 sous peine de ne pas fonctionner, à cause de certaine notation ex: lignes 202.


import sys      # importation du module permetant de manipuler différentes parties de l'environnement d'exécution Python.
import random   # importation du module générant des nombres/chiffres aléatoire.


##############  CONFIGURATION  ##############

sys.setrecursionlimit(10100)    # méthode permettant de dépasser la limite requise pour la récursion. 

class colors:      
    BLUE = '\033[36m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    PURPLE = '\033[95m'
    MAGENTA = '\033[35m'
    WHITE = '\033[37m'
    GRAY = '\033[30m'
    MINE = '\033[1;91m'
    RESET = '\033[0m'
    LST = [WHITE, BLUE, GREEN, YELLOW, PURPLE, MAGENTA, GRAY, GRAY, GRAY, MINE, RESET]
    
    
# ------------------------------------------------- Fonctions -------------------------------------------------


def create_board(n: int, m: int) -> list[list[str]]:
    """
    But : Construit un tableau de taille n x m où chaque case contient le caractère correspondant à une case inexporée.
    """
    board = [["."] * m for _ in range(n)]
    return board


def print_board(board: list[list[str]]) -> None:
    """
    But : Affiche le plateau de jeu de taille minimale 4x4 et maximale 100x100.
    """
    if 4 <= len(board) <= 100 and 4 <= len(board[0]) <= 100:    # condition pour l'affichage 
        n, m = get_size(board)
        print("    ", end="")
        for i in range(m):                                      # AFFICHAGE DE LA PREMIERE LIGNE : 
            if i >= 10:                                         # si (i) est un nombre 
                print(" " + str(i // 10), end="")               # on affiche seulement la dizaine
            else:
                print("  ", end="")
        print()
        print("    ", end="")
        for i in range(m):                                      # AFFICHAGE DE LA SECONDE LIGNE : 
            print(" " + str(i % 10), end="")                    # on affiche seulement l'unité de (i)
        print()                                                 
        print("   " + "-" * m * 2 + "---", end="")              # ligne de tiret en fonction de la taille de la matrice
        print()
        for i in range(n):
            if i >= 10:                                         # si (i) est un nombre : 
                print(str(i) + " |", end="")                    # on affiche (i) 
            else:                                               # sinon : 
                print(" " + str(i) + " |", end="")              # on affiche (i) avec un espace devant
            for j in range(m):
                print(color_board(board[i][j]), end="")         # affichage du contenue de la matrice à l'aide de la fct (color_board)
            print(" |", end="")
            print()
        print("   " + "-" * m * 2 + "---", end="")              # ligne de tiret en fonction de la taille de la matrice
        print("\n")


def color_board(element: str) -> str:
    """
    But : Gestion des couleurs lors de l'affichage du tableau de jeu.
    """
    if element != 'X' and element != '.' and element != 'F':        # si 'element' est un chiffre nous nous basons sur la liste 'LST' pour déterminer sa couleur
        return colors.LST[int(element)] + " " + str(element) + colors.RESET
    elif element == '.':                                            # si 'element' est un point '.' alors la couleur attribué est blanche
        return colors.WHITE + " " + str(element) + colors.RESET
    else:                                                           # sinon la couleur est rouge + écriture en gras (bold)
        return colors.MINE + " " + str(element) + colors.RESET


def get_size(board: list[list[str]]) -> tuple[int, int]:
    """
    But : Renvoie un tuple de deux entiers (n, m) correspondant aux dimensions du plateau donné en entrée.
    """
    lignes, colonnes = len(board), len(board[0])    
    return lignes, colonnes                         


def get_neighbors(board: list[list[str]], pos_x: int, pos_y: int) -> list[tuple[int, int]]:
    """
    But : Renvoie une liste de tuples où chaque tuple correspond à une case voisine de la case (pos_x, pos_y).
    """
    x, y = pos_x, pos_y
    n, m = get_size(board)
    # tous les voisins de (pos_x, pos_y) sont contenue dans la liste (proxi) :
    proxi = [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y), (x - 1, y + 1), (x - 1, y - 1), (x + 1, y + 1), (x + 1, y - 1)]
    neighbors = [i for i in proxi if 0 <= i[0] < n and 0 <= i[1] < m]   # vérifie que les voisins donnée soit bien contenue dans les dimensions de la matrice 
    return neighbors                                                    # ajoute les éléments valide dans une liste (neighbors)


def place_mines(reference_board: list[list[str]], number_of_mines: int, first_pos_x: int, first_pos_y: int) -> list[tuple[int, int]]:
    """
    But : Place aléatoirement les mines sur le plateau (reference_board) après que le joueur ait choisi une première case à dévoiler.
          Renvoie la liste des cases contenant une mine.
    """
    n, m = get_size(reference_board)
    case_invalide = get_neighbors(reference_board, first_pos_x, first_pos_y)    # comme son nom l'indique, cette liste contient les positions 
    case_invalide.append((first_pos_x, first_pos_y))                            # où les mines ne peuvent pas se retrouver
    mines_list = []
    while len(mines_list) < number_of_mines:                                    # -boucle qui se termine seulement si le nbr de mines voulu est atteint
        mine = random.randint(0, n - 1), random.randint(0, m - 1)               # -création d'un tuple en àléatoire à l'aide du module random
        if mine not in case_invalide and mine not in mines_list:                # -verifie que le tuple donné n'est pas présent dans 'case_invalide'
            reference_board[mine[0]][mine[1]] = 'X'                             #  mais également dans les tuples donné précédemment ! 
            mines_list.append(mine)                                             # -la board de reference (reference_board) contient désormais les mines
    return mines_list                                                           # -les mines valide sont ajouté à la liste (mines_list)


def fill_in_board(reference_board: list[list[str]]) -> None:
    """
    But : Permet de calculer le nombre de mines présentes dans le voisinage de chaque case.
          Cette fonction modifie ensuite le plateau de référence (reference_board) pour y faire apparaître ces nombres.
    """
    n, m = get_size(reference_board)                                 # -nous testons élément par élément avec (i, j)  
    for i in range(n):                                               # -s'il sagit d'une mine 'X' :
        for j in range(m):                                           #   -nous regardons les voisins de (i, j) dans la board grâce à l'appel de (get_neighbors)
            if reference_board[i][j] == 'X':                         #   -si nous retrouvons '.', c'est qu'il n'y a pas d'autres mines dans les alentours
                for proxi in get_neighbors(reference_board, i, j):   #      alors la board de reference contient désormais le chiffre '1' 
                    if reference_board[proxi[0]][proxi[1]] == '.':   #   -s'il n'y a ni 'X' ni '.', par élimination nous savons qu'il sagit d'un nombre
                        reference_board[proxi[0]][proxi[1]] = '1'    #      ce qui signifie qu'une mine est proche des voisins de la mine que nous testons
                    elif reference_board[proxi[0]][proxi[1]] != 'X': #      alors la board de reference contient désormais : 'chiffre déjà présent + 1'
                        reference_board[proxi[0]][proxi[1]] = str(int(reference_board[proxi[0]][proxi[1]]) + 1)
            elif reference_board[i][j] == '.':                        # -s'il sagit d'une case inexploré '.' :
                reference_board[i][j] = '0'                           #   alors la board de reference contient désormais le chiffre '0' 
    return None                                                       #   puisqu'il n'y aucune mine ! 


def propagate_click(game_board: list[list[str]], reference_board: list[list[str]], pos_x: int, pos_y: int) -> None:
    """
    But : Permet de mettre à jour le plateau de jeu en dévoilant d’un coup toutes les cases adjacentes à la case dévoilée après un clic,
          lorsque celles-ci n’ont aucune mine dans leur voisinage.
    """
    if reference_board[pos_x][pos_y] == '0':
        for i in get_neighbors(reference_board, pos_x, pos_y):                      # -nous regardons les voisins de la case dévoilé
            if game_board[i[0]][i[1]] == '.':                                       # -la case en question doit être inexploré sur le game board
                if reference_board[i[0]][i[1]] == '0':                              # -si l'un des voisins est une case '0' : 
                    game_board[i[0]][i[1]] = reference_board[i[0]][i[1]]            #   on l'a devoile 
                    propagate_click(game_board, reference_board, i[0], i[1])        #   répétition de l'opération avec une récurence
                elif reference_board[i[0]][i[1]] != 'X':                            # -si l'un des voisins n'est ni une case '0' ni 'X' : 
                    game_board[i[0]][i[1]] = reference_board[i[0]][i[1]]            #   alors c'est une case contenant un chiffre
    return None                                                                     #   on la dévoile


def parse_input(n: int, m: int) -> tuple[str, int, int]:
    """
    But : Permet au joueur de rentrer une chaîne de caractères selon un certain format.
          Celle-ci sera ensuite interprété et découpé en un tuple, où l'action peut être soit “c” soit “f” 
          et où (pos_x) et (pos_y) sont des entiers correspondant à la case visée par l’action.
    """
    print("\n")
    demande = input("Choix d'une case: ").lower()   # récupère l'input du joueur
    demande = demande.split()                       # transforme la demande en list[str] afin  d'utiliser chaques éléments à notre guise
    if len(demande) == 3 and (demande[0] == 'f' or demande[0] == 'c') and 0 <= int(demande[1]) < n and 0 <= int(demande[2]) < m:    # condition
        action, pos_x, pos_y = demande      
        pos_x, pos_y = int(pos_x), int(pos_y)
        return action, pos_x, pos_y
    else:                                        # si la condition n'est pas respecté alors un message d'erreur apparait avec les indications à suivre : 
        print('\033[1;91m' + "Veuillez choisir une case situé dans les dimensions du plateau({0}x{1})".format(n, m) + '\033[0m') 
        print('\033[1;91m' + "Les seuls actions possibles sont 'f' pour 'flags' et 'c' pour 'dévoiler'" + '\033[0m')
        print('\033[1;91m' + "Exemple : 'f x y'   ou   'c x y' " + '\033[0m')
        return parse_input(n, m)                 # donne la possibilité qu joueur de retenter un input grâce à la récursivité ! 


def check_win(game_board: list[list[str]], reference_board: list[list[str]], mines_list: list[tuple], total_flags: int) -> bool:
    """
    But : Vérifie les conditions de victoire et met fin au jeu lorsque au moins l’une de celle-ci est remplie.
    """
    n, m = get_size(reference_board)
    unexplored_list = [(i, j) for i in range(n) for j in range(m) if game_board[i][j] == '.']   # création d'une liste contenant la position de toutes les cases inexploré
    flags_list = [(i, j) for i in range(n) for j in range(m) if game_board[i][j] == 'F']        # [...] de tous les flags
    res = False
    if sorted(flags_list) == sorted(mines_list) and total_flags == len(mines_list):     # première condition de win
        res = True
    elif sorted(unexplored_list) == sorted(mines_list) and total_flags == 0:            # seconde condition de win 
        res = True
    return res


def init_game(n: int, m: int, number_of_mines: int) -> list[list[str]] | list[list[str]] | list[tuple[int,int]]:
    """
    But : À partir d'uniquement les dimensions du plateau et du nombre de mines souhaité, 
          initialise les paramètres du jeu en faisant appel aux fonctions définies précédemment. 
    """
    game_board = create_board(n, m)             # création du (game_board)
    reference_board = create_board(n, m)        # [...] (reference_board)
    demande = parse_input(n, m)                 # la variable (demande) récupère l'input du joueur
    mines_list = []
    if demande[0] == 'c':   # condition : l'action demandé par le joueur doit être de dévoiler
        mines_list = place_mines(reference_board, number_of_mines, demande[1], demande[2])
        for i in mines_list:
            reference_board[i[0]][i[1]] = 'X'       # le (reference_board) contient desormait les mines
        fill_in_board(reference_board)              # modifie (reference_board) pour y faire apparaitre le nombre de mines présentes dans le voisinage des cases
        propagate_click(game_board, reference_board, demande[1], demande[2])    # dévoile les cases autour de la position initial 
        return game_board, reference_board, mines_list
    else:                                           # si la condition n'est pas respecté alors un message d'erreur apparait avec les indications à suivre : 
        print('\033[1;91m' + "La première case à dévoiler doit s'écrire de la manière suivante : 'c x y' " + '\033[0m')
        return init_game(n, m, number_of_mines)     # donne la possibilité au joueur de retenter un input grâce à la récursivité ! 


def print_game(cas: int, board: list[list[str]], flags_list: list[tuple[int, int]], number_of_mines: int) -> None:
    """
    But :  Affichage du jeu dans sa globalité, avec des messages personnalisés en fonction de la situation (cas).
    """
    # chaque 'cas' correspont à une situation : win / defaite / flags>limite / erreur de jeu 
    if cas >= 0:
        print("Flags/Mines : " + str(len(flags_list)) + "/" + str(number_of_mines))
        print_board(board)
        if cas == 1:
            print('\033[1;91m' + "Vous avez perdu !")
            print("\n")
        if cas == 2:
            print('\033[92m' + "Vous avez gagné !")
            print("\n")
    elif cas == -1:
        print('\033[1;91m' + "Veuillez choisir une case inexploré" + '\033[0m') 
    else:
        print('\033[1;91m' + "Nombre maximum de drapeaux atteint" + '\033[0m')
    return None
                
              
# -------------------------- Main --------------------------    
              
              
def main() -> int:
    """
    But : Fonction principale qui permet le fonctionnement du jeu grâce aux appels des fonctions définies précédemment.
    """
    # 'argv' récupère les valeurs transmises lors de l'appel du programme :
    n, m, number_of_mines = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    game_board, reference_board, mines_list = init_game(n, m, number_of_mines)      # initialisation de la partie avec les paramètres
    print_board(game_board)
    win = False
    
    while not win:                                                                              # boucle qui se termine lorsque la partie est gagnée
        demande = parse_input(n, m)                                                             # recupère l'input du joueur
        flags_list = [(i, j) for i in range(n) for j in range(m) if game_board[i][j] == 'F']    # liste contenant la position de toutes les flags
        if demande[0] == 'c':     # ACTION DE DEVOILER
            if reference_board[demande[1]][demande[2]] == 'X': # dévoile une mine ---> défaite
                game_board[demande[1]][demande[2]] = 'X'
                print_game(1, game_board, flags_list, number_of_mines)                             # affichage du jeu 
                break                                                                              # sort de la boucle car partie perdu
            elif game_board[demande[1]][demande[2]] == '.':   
                game_board[demande[1]][demande[2]] = reference_board[demande[1]][demande[2]]       # dévoile la case
                propagate_click(game_board, reference_board, demande[1], demande[2])               # propagation de click
                print_game(0, game_board, flags_list, number_of_mines)                             # [...]
            else:
                print_game(-1, game_board, flags_list, number_of_mines)                            # message d'erreur
        elif demande[0] == 'f':     # ACTION DE FLAG
            if game_board[demande[1]][demande[2]] == '.':
                if len(flags_list) >= number_of_mines:                                      
                    print_game(-2, game_board, flags_list, number_of_mines)                        # message d'erreur
                else:                                                                              # pose une flags sur la position demandé                                          
                    game_board[demande[1]][demande[2]] = 'F'                                       
                    flags_list = [(i, j) for i in range(n) for j in range(m) if game_board[i][j] == 'F']
                    print_game(0, game_board, flags_list, number_of_mines)                         # [...]
            elif game_board[demande[1]][demande[2]] == 'F':                                        # si une flag est déjà présente ---> action de dé-flags
                game_board[demande[1]][demande[2]] = '.'
                flags_list = [(i, j) for i in range(n) for j in range(m) if game_board[i][j] == 'F']
                print_game(0, game_board, flags_list, number_of_mines)                             # [...]
            else:
                print_game(-1, game_board, flags_list, number_of_mines)             # message d'erreur
        win = check_win(game_board, reference_board, mines_list, len(flags_list))   # vérifie la condition de victoire après chaque coup joué
        
    if win:
        print_game(2, reference_board, flags_list, number_of_mines)     # affiche le plateau de jeu au complet
        return 1    # victoire
    else:
        return 0    # défaite


# ------------------------------------------------- Corps du code -------------------------------------------------
    
if __name__ == "__main__":
    main()