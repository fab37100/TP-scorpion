import math
import config


# region Définition des fonctions de calcul

# 1. equation Ressort K
def ressortK(e, v):
    # return 1 / 3 * (e / (1 - 2 * v))
    return (e / (1 - 2 * v)) / 3


# 2. Longueur à vide (en m)
def longueurVideLv(lb, lc):
    a = math.pow(lb, 2) - math.pow(lc, 2)
    return math.sqrt(a) / 2 if a >= 0 else 0


# 3. Longueur du déplacement ld (en m)
def longueurDeplacementLd(lf, lv):
    return lf - lv


# 4. Masse du projectile mp (en kg)
def masseProjectileMp(rho, d, lf):
    return rho * math.pi * math.pow((d / 2), 2) * lf


# 5. Vélocité V (en m/s)
def velociteV(k, ld, mp):
    return math.sqrt(k * math.pow(ld, 2) / mp)


# 6. Portée P (en m)
def porteeP(v, g, alpha):
    return math.pow(v, 2) / g * math.sin(math.radians(alpha) * 2)


# 7. Energie d'impact (en joules), assimilée à la force cinétique transformée à l'impact ec
def energieImpactEc(mp, v):
    return 1 / 2 * mp * math.pow(v, 2)


# 8. Equivalence Joule et gramme de TNT
def TNT(ec):
    return ec / 4184


# 9. Moment quadratique du bras I (en m4)
def quadriqueBrasI(b, h):
    return (b * math.pow(h, 3)) / 12


# 10. Force de traction F (en N)
def forceTractionF(k, ld):
    return k * ld


# 11. Flèche du bras f max
def flecheBrasMaxf(f, e, i):
    return (f * math.pow(f, 3)) / (48 * e * i)


# endregion

# region Limites

# 9. Moment quadratique du bras I (en m4)
def quadratiqueBras(b, h):
    return (b * math.pow(h, 3)) / 12


# 10. Force de traction F (en N)
def forcetraction(k, ld):
    return k * ld


# 11. Flèche du bras f max
def flecheBras(f, lb, e, l):
    return (f * math.pow(lb, 3)) / (48 * e * l)


# endregion

# Defini et calcul toutes les règles métier deisponible dans le TP
# La portée, la TNT, la longueur de déplacement et le bras max de la flèche par individu est retourné par la fonction
def regleMetierIndividu(individu):
    calcul_ressort = ressortK(individu[7], individu[8])
    calcul_longueur_vide = longueurVideLv(individu[1], individu[4])
    calcul_longueur_deplacement = longueurDeplacementLd(individu[5], calcul_longueur_vide)
    calcul_masse_projectile = masseProjectileMp(individu[6], individu[9], individu[5])
    calcul_velocite = velociteV(calcul_ressort, calcul_longueur_deplacement, calcul_masse_projectile)
    calcul_portee = porteeP(calcul_velocite, config.GRAVITE_TERRE, individu[0])
    calcul_energie = energieImpactEc(calcul_masse_projectile, calcul_velocite)
    calcul_tnt = TNT(calcul_energie)
    calcul_quadriqueBras = quadriqueBrasI(individu[9], individu[10])
    calcul_forceTraction = forceTractionF(calcul_ressort, calcul_longueur_deplacement)
    calcul_flecheBrasMax = flecheBrasMaxf(calcul_forceTraction, individu[7], calcul_quadriqueBras)

    return [calcul_portee, calcul_tnt, calcul_longueur_deplacement, calcul_flecheBrasMax]


# Cette fonction Normale adaptée pour le scorpion, permet d'evualer le score de la portée d'un individu evalue sur le
# paramètre MAX_SCORE_FITNESS
# 0.05 est ajoute au score final afin d'eviter de mettre un score de 0 au individu tirant loin de la cible
def fonctionNormale(x, u):
    # Le sigma est divisé par 20 afin d'avoir une courbe exponentielle importante
    sigma = u / 20
    f = (math.exp(-1 / 2 * math.pow(((x - u) / sigma), 2))) * config.MAX_SCORE_FITNESS + 0.05
    return f


def calculVarianceScore(score_individus, score_moyenne):
    return