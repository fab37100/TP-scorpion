import random
import config
import maths


# region Definitions de genes
def geneAngleHausse():
    return random.uniform(config.MIN_ANGLE_HAUSSE, config.MAX_ANGLE_HAUSSE)


def geneLongueurBras():
    return random.uniform(config.MIN_LONGUEUR_BRAS, config.MAX_LONGUEUR_BRAS)


def geneSectionBras():
    return random.uniform(config.MIN_SECTION_BRAS, config.MAX_SECTION_BRAS)


def geneHauteurSection():
    return random.uniform(config.MIN_HAUTEUR_SECTION, config.MAX_HAUTEUR_SECTION)


def geneLongueurCorde():
    return random.uniform(config.MIN_LONGUEUR_CORDE, config.MAX_LONGUEUR_CORDE)


def geneLongueurFleche():
    return random.uniform(config.MIN_LONGUEUR_FLECHE, config.MAX_LONGUEUR_FLECHE)


def geneMasseVolFleche():
    return random.uniform(config.MIN_MASSE_VOL_FLECHE, config.MAX_MASSE_VOL_FLECHE)
    # return 7860


def geneYoungMateriau():
    return random.uniform(config.MIN_YOUNG_MATERIAU, config.MAX_YOUNG_MATERIAU)
    # return 208


def geneCoefPoisson():
    return random.uniform(config.MIN_COEF_POISSON, config.MAX_COEF_POISSON)
    # return 0.22


def geneBaseFleche():
    return random.uniform(config.MIN_BASE_FLECHE, config.MAX_BASE_FLECHE)


def geneHauteurFleche():
    return random.uniform(config.MIN_HAUTEUR_FLECHE, config.MAX_HAUTEUR_FLECHE)


# endregion


# Creation de la population avec les parametres de configuration defini dans le fichier config.py
def creationPopulation():
    # return [51, 29.9, 9.7, 9.1, 2, 0.5, 0.2, 210, 0.27, geneBaseFleche(), geneHauteurFleche()]
    return [
        geneAngleHausse(),  # 0
        geneLongueurBras(),  # 1
        geneSectionBras(),  # 2
        geneHauteurSection(),  # 3
        geneLongueurCorde(),  # 4
        geneLongueurFleche(),  # 5
        geneMasseVolFleche(),  # 6
        geneYoungMateriau(),  # 7
        geneCoefPoisson(),  # 8
        geneBaseFleche(),  # 9
        geneHauteurFleche()  # 10
    ];


# Evaluation des individus
def evaluationIndividu(individu):
    # variable : regle_metier_individu
    #       0               1                   2                   3
    # calcul_portee, calcul_tnt, calcul_longueur_deplacement, calcul_flecheBrasMax
    regle_metier_individu = maths.regleMetierIndividu(individu)
    distance = abs(config.DISTANCE_CIBLE - regle_metier_individu[0])

    score_individu = scoreIndividu(regle_metier_individu[0], regle_metier_individu[1], regle_metier_individu[2],
                                   regle_metier_individu[3])
    # print("Portée : " + str(regle_metier_individu[0]) + " | Distance : " + str(distance) + "  | TNT : " + str(
    #     regle_metier_individu[1]) + "  | Score : " + str(score_individu))

    # Le score de l'individu est renvoyé ainsi que sa portee et sa tnt
    return [score_individu, regle_metier_individu[0], regle_metier_individu[1]]


# Calcul du score pour chaque individu en fonction des limites
def scoreIndividu(calcul_portee, calcul_tnt, calcul_longueur_deplacement, calcul_flecheBrasMax):
    # Le score de l'individu est : la portée de l'invidu + sa puissance exprimée en TNT
    # Concernant le score de la portée, elle est attribuée avec une fonction "Normale" légérement modifiée et evaluée sur score de 1000
    # Si un individu tire à moins de 50cm de la cible alors un boost de 1000 point lui est attribué
    if abs(calcul_portee - config.DISTANCE_CIBLE) <= 0.5:
        score_individu = maths.fonctionNormale(calcul_portee, config.DISTANCE_CIBLE) + calcul_tnt + 1000
    else:
        score_individu = maths.fonctionNormale(calcul_portee, config.DISTANCE_CIBLE) + calcul_tnt
    # Si le calcul de la longueur de déplacement et plus grand que le calcul de la fleche du bras maximum
    # Alors le scorpion ne peut pas tirer et ce voit attribuer un score infiniment petit sans l'exclure lors de la
    if calcul_longueur_deplacement > calcul_flecheBrasMax:
        score_individu = 0.001
    return score_individu


# Selection de parent avec la méthode RWS
def selectionParent(score_individu, individus):
    liste_couples = []
    while len(liste_couples) < config.NB_POPULATION / 2:
        parent = []
        k = 0
        while k < 2:
            # Définition de la valeur de selection RWS en fonction du score total des individus de la generation
            # Le score total est le dernier individu
            rws = random.uniform(0, score_individu[len(score_individu) - 1])
            for j in range(0, config.NB_POPULATION):
                if score_individu[j] > rws:
                    # Vérification que la selection ne choisit pas le même parent, Si c'est le cas alors le deuxième parent est redefini
                    if k == 1 and parent[0] == individus[j]:
                        # print(str(k) + "Parent A : " + str(parent[0]) + "   | Parent B : " + str(individus[j]))
                        break
                    else:
                        # Ajout d'un parent selectionné dans le tableau "parent"
                        parent.append(individus[j])

                        # print("parent " + str(len(parent)))
                        k += 1
                    break
        # Ajout du couple de parent dans une liste qui comprend tous les parents séléctionné par la méthode RWS
        liste_couples.append(parent)
    return liste_couples


# Création des enfants et application de la mutation
def creationEnfants(liste_couples):
    liste_enfants = {}
    for i in range(0, config.NB_POPULATION, 2):
        # print("liste : " + str(i))
        parents = int(i / 2)
        if random.randint(0, 11) <= config.COUPE_CROISEMENT:
            aleatoire_coupe = random.randint(0, 11)
            liste_enfants[i] = liste_couples[parents][0][:aleatoire_coupe] + liste_couples[parents][1][
                                                                             aleatoire_coupe:]
            liste_enfants[i + 1] = liste_couples[parents][1][:aleatoire_coupe] + liste_couples[parents][0][
                                                                                 aleatoire_coupe:]
        else:
            liste_enfants[i] = liste_couples[parents][0][:5] + liste_couples[parents][1][5:]
            liste_enfants[i + 1] = liste_couples[parents][1][:5] + liste_couples[parents][0][5:]

        # Mutation des enfants suivants le pourcentage dans la configuration
        for z in range(0, 2):
            if random.randint(0, 100) < config.POURCENTAGE_MUTATION:
                position_gene = random.randint(0, 10)
                # print("Random : " + str(position_gene))
                # print("Z : " + str(z))
                # print(len(liste_enfants))
                # print(liste_enfants[i + z])
                liste_enfants[i + z][position_gene] = creationPopulation()[position_gene]
                # print(liste_enfants[i + z])
                # print(liste_enfants[i])

    return liste_enfants