import random
from time import sleep
import json


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


def save_game(data_to_save, game_file) :
    with open(game_file, "w") as f:
        json.dump(data_to_save, f)
    print(f"Jeu sauvegardé ! Your data : {data_to_save}")


def load_game(data_to_save):
	with open(data_to_save, "r") as f:
		data_to_save = json.load(f)
	return data_to_save


# starting dice
def dice_base() :
    """
    None --> Int
    Retourne un random entre 1 et 6
    """

    dice_value = random.randint(1, 6)
    print(f"dé : {dice_value}")

    return dice_value



# throw dice, print and return its' value
# with 6 player goes again
def get_dice_val() :
    """
    None --> Int
    Retourne un random entre 1 et 6, relance quand c'est 6 et retourne la somme (limite 3 fois 6)
    """

    dice_value = dice_base()
    count = 0

    while dice_value % 6 == 0 and count != 3:
        print("Vous avez obtenu un 6, vous pouvez relancez !")
        input("Appuyez sur ENTER pour lancer le dé : ")

        dice_value += dice_base() 
        count += 1
    
    sleep(1)
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


def decide_order(player_doublons):
    """
    List -> List
    Fonction retournant l'ordre des joueurs sur un lancé de dé.
    """
    global sorted_tuples

    dict = {}
    order = []

    for player in player_doublons:
        print(f"\nLancez votre dé {player}!")
        input("Appuyer sur ENTER pour lancer le dé : ")
        dict[player] = dice_base()
        
    sorted_tuples = sorted(dict.items(), key=lambda item:item[1], reverse=True)    

    for key in sorted_tuples :
        order.append(key[0])

    return order


def print_player_doublons(player_doublons):
    n = len(player_doublons)

    if n == 2:
        print(f"\n[Départagez-vous {player_doublons[0]} et {player_doublons[1]}!]")
    
    elif n == 3:
        print(f"\n[Départagez-vous {player_doublons[0]}, {player_doublons[1]} et {player_doublons[2]}!]")

    else:
        print(f"\n[Départagez-vous {player_doublons[0]}, {player_doublons[1]}, {player_doublons[2]} et {player_doublons[3]}!]")


def doublons_exception(player_double):
    global sorted_tuples

    player_double1 = [player_double[0], player_double[1]]
    player_double2 = [player_double[2], player_double[3]]

    order_doublons1 = decide_order(player_double1)
    a = sorted_tuples
    order_doublons2 = decide_order(player_double2)
    a.append(sorted_tuples)
    sorted_tuples = a

    return [order_doublons1 + order_doublons2]


def who_starts(liste_joueurs):
    """
    List -> List
    Fonction retournant la liste de joueur dans l'ordre de qui a lancé le plus grand nombre.
    """

    # Decide order #1
    order = decide_order(liste_joueurs)
    
    while True:
        # Check doublons
        if verif_doublons(sorted_tuples):
            player_double = player_doublons(sorted_tuples)

            # Cas exceptionnel: quand il y a plusieurs doublons (ex: 2, 2, 4, 4)
            if len(player_double) == 4 and sorted_tuples[0][1] != sorted_tuples[-1][1]:
                order = doublons_exception(player_double)
                continue

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
    Int --> Int
    Fonction retournant le score du joueur si il est placé sur une case serpent.
    """

    print(f"Vous êtes tombés sur un serpent, dans la case numéro {score_joueur} ! ")
    score_joueur = serpents[score_joueur]
    print(f"Vous descendez à la case numéro {score_joueur} !\n")

    return score_joueur


# print these if player got echelle
def got_echelle(score_joueur):
    """
    Int --> Int
    Fonction retournant le score du joueur si il est placé sur une case échelle.
    """
    
    print(f"Vous êtes tombés sur une échelle, dans la case numéro {score_joueur} ! ")
    score_joueur = echelles[score_joueur]
    print(f"Vous montez à la case numéro {score_joueur} !\n")

    return score_joueur


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

# print score / map et plateau actuel
def affiche_plateau(plateau, ordre_joueur, pawn):
    
    print()
    # Player's name
    for pawn, player in zip(pawn, ordre_joueur):
        print(f"     {pawn} {player}", end = "")

    # Map
    for i, liste in enumerate(plateau):
        if i == 0:
            print(f"\n100 | {liste[0]}", end = " ")

        elif i % 2 == 0:
            print(f"\n {100 - i * 10} | {liste[0]}", end = " ")

        elif i == 9:
            print(f"\n  → | {liste[0]}", end = " ")

        else:
            print(f"\n  ↱ | {liste[0]}", end = " ")


        for colonne in liste[1:]:
            print(f"| {colonne}", end = " ")
            

        if i % 2 != 0:
            print("|", 100 - i * 10 , end = "")

        else:
            print("| ↰", end = "")
    print()


def replace(arr, find, replace):
    # fast and readable
    base = 0
    for cnt in range(arr.count(find)):
        offset = arr.index(find, base)
        arr[offset] = replace
        base = offset + 1


def update_plateau(plateau, player_case, pawn):
    for i in range(1, 11):
        if player_case <= i * 10:
            break
    
    for liste in plateau:
        replace(liste, pawn, " ")

    number = str(player_case)

    # Eventually 
    if player_case == 100:
        plateau[0][0] = pawn
        return

    if i % 2 == 0:
        if int(number[-1]) == 0:
            plateau[10 - i][0] = pawn
            return

        plateau[10 - i][10 - int(number[-1])] = pawn

    else:
        plateau[10 - i][int(number[-1]) - 1] = pawn


## Notes et problèmes ##
# /-\ who_starts: Exception quand il y a plusieurs doublons (ex: 2, 2, 4, 4). [A UPDATE]
# /!\ tracing_score permet de suivre le chemin d'une joueur. [PAS CODE]
# /!\ Save file [PAS CODE] serialisation desserlisation
# /-\ Map après chaque tour [PAS CODE]


# Les éléments primaires du jeu sont: le dé, le plateau et les effets des case (serpents et échelles).
# Les éléments secondaires sont: le mouvement, la condition de victoire, sélection des personnages et les difficultés.
# Int pour la position du joueur dans le jeu dans un dictionnaire.
# 12 fonctions pour le système | 3 fonctions pour l'interface | 1 fonction pour l'affichage
##


# setup
tracing_score = []
plateau = [[" " for n in range(10)] for m in range(10)]
pawn = ["➀", "➁", "➂", "➃"]


game_file = "jeu_d_echelles.json"

### Main ###
def game_with_bot():
    print("[JEU DES SERPENTS ET DES ECHELLES]\n")

    while True:
        number_bots = int(input("Entrez le nombre de bots que vous voulez jouer contre (max 3): "))

        if 1 < number_bots < 3:
            break
        print("Le nombre de bots doit être compris entre 1 et 3. Réessayez. \n")

    bots = ["Steve", "Eve", "Matt"]
    liste_joueurs = random.sample(bots, number_bots)

    print("\nPour décider de l'ordre, lancez le dé. \nCeux qui ont les scores les plus élevés passent en premier.")

    None


def game_no_bot(loaded_game):
    global game_file
    global data_to_save

    print("[JEU DES SERPENTS ET DES ECHELLES]\n")

    if loaded_game :
        player_name, player_pos, count_tour = zip(*data_to_save)
        # if the round was finished
        if all(x == count_tour[0] for x in count_tour) :
            ordre_joueur = list(player_name)
            score_joueur = list(player_pos)
        # if the round wasn't finished
        # new order of players --> those who didn't finish their round in the previous game go first
        # still according to the og order
        else :
            new_ordre = []
            players = len(data_to_save)
            while len(new_ordre) != players :
                new_ordre = [data_to_save[n] for n in range(1, players) if count_tour[0] != count_tour[n]]
                new_ordre.extend(x for x in data_to_save if x not in new_ordre)
                new_ordre = [list(t) for t in zip(*new_ordre)]
                ordre_joueur = new_ordre[0]
                score_joueur = new_ordre[1]
        count_tour = [0 for n in count_tour]

    else :
        liste_joueurs = select_player()

        print("\nPour décider de l'ordre, lancez le dé. \nCeux qui ont les scores les plus élevés passent en premier.")
        print("Le jeu commencera dans un instant.")
        sleep(3)
    
        ordre_joueur = who_starts(liste_joueurs)
        score_joueur = [0 for n in liste_joueurs]
        count_tour = [0 for n in liste_joueurs]

        print(f"\nVous pouvez commencer ! Ordre : {ordre_joueur} \n")

    running = True
    count = 0
    round = 1

    while running:
        for player_number, player_name in enumerate(ordre_joueur):

            # Set up player's score
            player_case = score_joueur[player_number]

            sleep(1)
            print(f"[Tour de {player_name}]")     

            # Select different commands
            while True: 
                ask = input("Appuyer sur ENTER pour lancer le dé : ")

                if ask == "":
                    dice = get_dice_val()
                    player_case += dice
                    break

                # To show the current progression / map
                elif ask == "map" or ask == "plateau":
                    affiche_plateau(plateau, ordre_joueur, pawn)
                
                # To save the game
                elif ask == "save":
                    save_game(data_to_save, game_file)
                    break
                
                else: 
                    print("[ERROR: Commande introuvable]")


            # Effects
            if player_case in serpents:
                player_case = got_serpent(player_case)

            elif player_case in echelles :
                player_case = got_echelle(player_case)
            
            else:
                print(f"Vous êtes arrivés à la case numéro {player_case}.\n")
            
            # If player score is beyond 100 then move backward from the case 100 of 100 - dice
            if player_case + dice > 100:
                player_case = need_exact_win(player_case)

            # Check win
            if check_win(player_case, player_name):
                running = False
            
            # Update score_joueur
            score_joueur[player_number] = player_case

            # Update plateau
            update_plateau(plateau, player_case, pawn[player_number])

            # save the position of each player in the order the go after each other
            positions = [score_joueur[player] for player in range(len(ordre_joueur))]
            
            # prints the end of round and the position of each player
            count += 1
            count_tour[player_number] += 1
            data_to_save = list(zip(ordre_joueur, positions, count_tour))
            if count == len(ordre_joueur) :
                count = 0
                sleep(1)
                print(f"[End of round {round}]")
                round +=1
                for n in range(len(ordre_joueur)) :
                    sleep(0.5)
                    print(f"{ordre_joueur[n]} vous etes sur la case {positions[n]}.")
                print("\n")



def choice_gamemode():
    global data_to_save
    
    # ask if player wants to load previous game
    while True :
        d = input("Voulez-vous continuer votre jeu précédent (o/n) ? ")
        
        if d.lower() =="o" or d.lower() == "n" :
            break
        print("[ERREUR] Commande invalide. Réessayez. \n")
        sleep(1)

    if d.lower() == "n" :
        loaded_game = False
        print("Vous commencez une nouvelle partie. \n")
    
    # if player asks to reload game, if there is a saved game it loads it
    # otherwise it starts a new game
    else :
        try :
            data_to_save = load_game(game_file)
            loaded_game = True
            print("Jeu précédent chargé avec succès.")
            print("\n[Mode local avec joueurs]")
        except :
            loaded_game = False
            print("[ERREUR] Aucun jeu précédent trouvé. \nVous commencez une nouvelle partie. \n")

    if loaded_game :
        game_no_bot(loaded_game)
    
    else :
        while True :
            print("Mode solo avec bots (0) Mode local avec joueurs (1)")

            a = input("Tapez un mode de jeu: ")

            if a == "0" or a == "1":
                break
            print("[ERREUR] Ce mode ne fait pas partie des modes de jeu. Réessayez. \n")
            sleep(1)

        if a == "0":
            print("\n[Mode solo avec bots]")
            game_with_bot()
    
        else:
            print("\n[Mode local avec joueurs]")
            game_no_bot(loaded_game)
    

# Commandes start
choice_gamemode()
