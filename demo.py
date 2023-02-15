import random
from time import sleep
from sys import exit

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


# setup
dice = 0
score_joueur = 0
tracing_score = []


# starting dice
def dice_base() :
    """
    None --> Int
    Retourne un random entre 1 et 6
    """
    input("\nTapez ENTER pour lancer le dé : ")
    dice_value = random.randint(1, 6)
    print(f"dé : {dice_value}")

    return dice_value


# throw dice, print and return its' value
# with 6 player goes again
def get_dice_val() :
    """
    None --> Int
    Retourne un random entre 1 et 6, relance quand c'est 6 et retourne la somme
    """
    dice_value = dice_base()

    return dice_value


# alternative if the player gets 6
def replay(relancer):
    """
    None --> None
    Permet de rejouer si le joueur a obtenu un 6 au dé
    """
    global score_joueur
    global relances
    if relancer != False :
        print("Vous avez obtenu un 6. Vous pouvez relancer !")
        dice = get_dice_val()
        #dice = 6 #test limite
        score_joueur += dice
        square_effect()
        tracing_score.append(score_joueur)
        check_win(score_joueur)
        if dice == 6 :
            if relances != 3 : #[limite]
                relances += 1
                replay(relancer)
            else :
                print("Vous avez atteint la limite de relancés")
    else :
        print("Vous êtes tomber sur un serpent donc vous ne pouvez pas relancer")


# print these if player got serpent
# eventually probably going to need the name of the player, to know who got it
def got_serpent(score_joueur):
    """
    (Str x) Int --> None
    """
    sleep(1)
    print("Vous êtes tombés sur un serpent ! ")
    print("Vous descendez à la case numéro {} !".format(score_joueur))


# print these if player got echelle
# eventually probably going to need the name of the player, to know who got it
def got_echelle(score_joueur):
    """
    (Str x) Int --> None
    """
    sleep(1)
    print("Vous êtes tombés sur une échelle ! ")
    print("Vous montez à la case numéro {} !".format(score_joueur))


# function to activate the square effect
def square_effect() :
    """
    None --> None
    Active l'effet de la case sur laquelle un joueur est tombé et annule
    le fait de pouvoir relancer si le joueur est tombé sur un serpent
    """
    global score_joueur
    global relancer

    print("Vous êtes arrivés à la case", score_joueur)
    if score_joueur in serpents :
        score_joueur = serpents[score_joueur]
        got_serpent(score_joueur)
        relancer = False

    elif score_joueur in echelles :
        score_joueur = echelles[score_joueur]
        got_echelle(score_joueur)
        relancer = True
    else :
        print("Heureusement cette case n'a aucun effet !")
        relancer = None


# what the name says
# eventually probably going to need the name of the player, to know who got it
def need_exact_win(score_joueur) :
    """
    """
    sleep(1)
    if score_joueur > 100 :
        score_joueur = 100 - (score_joueur - 100)
        print(f"Vous ne pouvez pas dépasser l'arrivée, donc vous êtes retourné(e)s à la case {score_joueur}")
    return score_joueur


# eventually probably going to need the name of the player, to know who got it
def check_win(score_joueur) :
    """
    """
    if score_joueur == 100 :
        print("Vous avez gagné !") #add winner name here too
        print("Voici le chemin que vous avez effectué durant la partie : ", tracing_score)
        exit("The End")


while dice != 6 :
    dice = dice_base()
    #dice = 6 #test

sleep(1)
print("\nVous pouvez commencer ! ")
score_joueur = 1

while score_joueur < 100 :
    dice = get_dice_val()
    #dice = 2 #test échelle
    #dice =3 #test neutre
    #dice = 6 #test relancer
    score_joueur += dice

    score_joueur = need_exact_win(score_joueur)

    square_effect()

    print("score du joueur :", score_joueur)

    tracing_score.append(score_joueur)

    check_win(score_joueur)

    if dice == 6 :
        relances = 1
        replay(relancer)
