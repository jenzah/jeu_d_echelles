
import random
from time import sleep


echelles = {
    3  : 17,
    13 : 28,
    18 : 37,
    32 : 53,
    36 : 63,
    42 : 61,
    65 : 75,
    69 : 72,
    84 : 99,
    89 : 94
}

serpents = {
    9  : 6,
    24 : 16,
    29 : 10,
    39 : 1,
    46 : 44,
    51 : 48,
    56 : 47,
    67 : 45,
    77 : 58,
    87 : 68,
    92 : 85,
    97 : 26,
}



# starting dice
def dice_base(bots = False) :
    """
    None --> Int
    Retourne un random entre 1 et 6
    """
    if not bots :
        input("Tapez ENTER pour lancer le dé : ")
    else :
        if player_name != "Joueur" :
            sleep(1)
            print("Tapez ENTER pour lancer le dé : ")
            sleep(1)
        else :
            input("Tapez ENTER pour lancer le dé : ")

    dice_value = random.randint(1, 6)
    print(f"dé : {dice_value}")

    return dice_value


# throw dice, print and return its' value
# with 6 player goes again
def get_dice_val(bots = False) :
    """
    None --> Int
    Retourne un random entre 1 et 6, relance quand c'est 6 et retourne la somme (limite 3 fois 6)
    """
    if bots :
        dice_value = dice_base(bots = True)
    else :
        dice_value = dice_base()
    count = 0

    while dice_value % 6 == 0 and count != 3:
        print("Vous avez obtenu un 6, vous pouvez relancez !")


        if bots :
            dice_value += dice_base(bots = True)
        else :
            dice_value += dice_base()
        count += 1

    print(f"Vous avancez de {dice_value}.")

    return dice_value


# To get the name of the players
def get_noms_joueurs() :
    """
    None -> Str
    Fonction retournant le nom (str) d'un joueur.
    """

    joueur_nom = None
    while not joueur_nom :
        joueur_nom = input(f"Entrez un nom du joueur {i + 1}: ")

        if joueur_nom in LISTE_JOUEUR:
            print("Ce nom a déjà été pris. Réessayez.")
            joueur_nom = None

    return joueur_nom


# To get the number of player and their names (game of 2 to 4 players)
def select_player():
    """
    None -> List
    Fonction retournant la liste des joueurs.
    """

    global LISTE_JOUEUR
    global i

    LISTE_JOUEUR = []

    while True :
        number = int(input("Entrez le nombre de joueur (2 à 4 joueurs): "))

        if 2 <= number <= 4:
            break

    for i in range(number) :
        LISTE_JOUEUR.append(get_noms_joueurs())

    return LISTE_JOUEUR


###
def verif_doublons(pack):
    """
    List -> Bool
    """

    for index, couple in enumerate(pack):
        for couple2 in pack[index + 1:]:
            if couple[1] in couple2:
                return True
    return False


def player_doublons(pack):
    """
    List -> List
    Fonction retournant la liste des joueurs avec un doublons de dé.
    """

    numbers = []
    players = []
    players_doublons = []

    # To unpack the package (player, number)
    players, numbers = zip(*pack)

    # To find players with doublons
    for index, number in enumerate(numbers):
        if number in numbers[index + 1:] or number in numbers[:index]:
            players_doublons.append(players[index])

    return players_doublons


def decide_order(player_doublons, bots = False):
    """
    List -> List
    Fonction retournant l'ordre des joueurs sur un lancé de dé.
    """
    global sorted_tuples
    global player_name

    dict = {}
    order = []

    for player in player_doublons:
        print(f"\n[{player}]")
        if bots :
            player_name = player
            dict[player] = dice_base(bots = True)
        else:
            dict[player] = dice_base()

    sorted_tuples = sorted(dict.items(), key=lambda item:item[1], reverse=True)

    for key, value in sorted_tuples :
        order.append(key)

    return order


def print_player_doublons(player_doublons):
    n = len(player_doublons)

    if n == 2:
        print(f"\nDépartagez-vous {player_doublons[0]} et {player_doublons[1]}!")

    elif n == 3:
        print(f"\nDépartagez-vous {player_doublons[0]}, {player_doublons[1]} et {player_doublons[2]}!")

    else:
        print(f"\nDépartagez-vous {player_doublons[0]}, {player_doublons[1]}, {player_doublons[2]} et {player_doublons[3]}!")


def who_starts(liste_joueurs, bots = False):
    """
    List -> List
    Fonction retournant la liste de joueur dans l'ordre de qui a jeté le plus grand nombre.
    """

    # Decide order #1
    if bots :
        order = decide_order(liste_joueurs, bots = True)
    else :
        order = decide_order(liste_joueurs)

    while True:
        # Check doublons
        if verif_doublons(sorted_tuples):
            player_double = player_doublons(sorted_tuples)

            if len(player_double) == 4:
                None
            # Decide order #2
            print_player_doublons(player_double)
            order_doublons = decide_order(player_double)

            n = len(order_doublons)
            # Change order
            for i in range(len(order) - 1):
                if set(order[i : i + n]) == set(order_doublons):
                    for count, x in enumerate(order_doublons):
                        order[i + count] = x

        else:
            break

    return order
###


# print these if player got serpent
def got_serpent(score_joueur):
    """
    Int --> None
    Procédure changeant le score du joueur si il est placé sur une case serpent.
    """

    score_joueur = serpents[score_joueur]

    print("Vous êtes tombés sur un serpent ! ")
    print(f"Vous descendez à la case numéro {score_joueur} !\n")


# print these if player got echelle
def got_echelle(score_joueur):
    """
    Int --> None
    Procédure changeant le score du joueur si il est placé sur une case échelle.
    """

    score_joueur = echelles[score_joueur]

    print("Vous êtes tombés sur une échelle ! ")
    print(f"Vous montez à la case numéro {score_joueur} !\n")


### If the player draws a number that makes him go beyond the score 100 he moves back to 100-number
def need_exact_win(score_joueur) :
    """
    Int -> Int
    Fonction retournant le score du joueur si il dépasse la case 100 (100 - num).
    """

    sleep(1)
    if score_joueur > 100 :
        score_joueur = 100 - (score_joueur - 100)
        print(f"Vous ne pouvez pas dépasser l'arrivée, donc vous êtes retourné(e)s à la case {score_joueur}\n")
    return score_joueur


def check_win(score_joueur, player_name) :
    """
    """
    if score_joueur == 100 :
        print(f"Vous avez gagné {player_name}!")
        print("Voici le chemin que vous avez effectué durant la partie : ", tracing_score)

        return True
    return False
###


## Notes et problèmes ##
# /!\ who_starts: Exception quand tous 2 joueurs ont des doublons avec 2 autres joueurs avec des doublons. [A CORRIGER]
# /!\ tracing_score permet de suivre le chemin d'une joueur. [PAS CODE]
# /!\ Save file [PAS CODE]


# Les éléments primaires du jeu sont: le dé, le plateau et les effets des case (serpents et échelles).
# Les éléments secondaires sont: le mouvement, la condition de victoire, sélection des personnages et les difficultés.
# Int pour la position du joueur dans le jeu dans un dictionnaire.
# 12 fonctions pour le système | 3 fonctions pour l'interface | 1 fonction pour l'affichage
##

# setup
tracing_score = []


### Main ###
def game_with_bots():
    print("[JEU DES SERPENTS ET DES ECHELLES]\n")

    global player_name

    while True:
        number_bots = int(input("Entrez le nombre de bots que vous voulez jouer contre (max 3): "))

        if 1 <= number_bots <= 3:
            break
        print("Le nombre de bots doit être compris entre 1 et 3. Réessayez. \n")

    bots = ["Steve", "Eve", "Matt"]
    liste_joueurs = random.sample(bots, number_bots)
    liste_joueurs.insert(0, "Joueur")

    print("\nPour décider qui commencera, lancez le dé. \nCelui qui a le score le plus élevé commence.")

    ordre_joueur = who_starts(liste_joueurs, bots = True)

    print(f"\nVous pouvez commencer ! Ordre : {ordre_joueur}\n ")

    score_joueur = [0 for n in liste_joueurs]
    running = True

    while running:
        for player_number, couple in enumerate(ordre_joueur):

            # Set up player's score and name
            player_case = score_joueur[player_number]
            """ player_name = couple[0] """
            player_name = couple

            print(f"Tour de [{player_name}]")

            dice = get_dice_val(bots = True)
            player_case += dice

            # Effects
            if player_case in serpents:
                got_serpent(player_case)

            elif player_case in echelles :
                got_echelle(player_case)

            else:
                print(f"Vous êtes arrivés à la case numéro {player_case}.\n")

            # If player score is beyond 100 then move backward from the case 100 of 100 - dice
            if player_case + dice > 100:
                player_case = need_exact_win(player_case)

            # Check win
            tracing_score.append(player_case)

            if check_win(player_case, player_name):
                running = False

            # Update score_joueur
            score_joueur[player_number] = player_case

    None


def game_no_bot():
    print("[JEU DES SERPENTS ET DES ECHELLES]\n")

    liste_joueurs = select_player()

    print("\nPour décider qui commencera, lancez le dé. \nLe joueur qui obtient le score le plus élevé commence.")

    ordre_joueur = who_starts(liste_joueurs)

    print(f"\nVous pouvez commencer ! Ordre : {ordre_joueur}\n ")

    score_joueur = [0 for n in liste_joueurs]
    running = True

    while running:
        for player_number, couple in enumerate(ordre_joueur):

            # Set up player's score and name
            player_case = score_joueur[player_number]
            """ player_name = couple[0] """
            player_name = couple

            print(f"Tour de [{player_name}]")

            dice = get_dice_val()
            player_case += dice

            # Effects
            if player_case in serpents:
                got_serpent(player_case)

            elif player_case in echelles :
                got_echelle(player_case)

            else:
                print(f"Vous êtes arrivés à la case numéro {player_case}.\n")

            # If player score is beyond 100 then move backward from the case 100 of 100 - dice
            if player_case + dice > 100:
                player_case = need_exact_win(player_case)

            # Check win
            tracing_score.append(player_case)

            if check_win(player_case, player_name):
                running = False

            # Update score_joueur
            score_joueur[player_number] = player_case


def choice_gamemode():
    print("Mode solo avec bots (0) Mode local avec joueurs (1)")

    while True:
        a = input("Tapez un mode de jeu: ")

        if a == "0" or a == "1":
            break
        print("Ce mode ne fait pas partie des modes de jeu. Réessayez. \n")
        sleep(1)

    if a == "0":
        print("\n[Mode solo avec bots]")
        game_with_bots()

    else:
        print("\n[Mode local avec joueurs]")
        game_no_bot()

# Commandes start
choice_gamemode()
