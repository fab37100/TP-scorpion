import config
import fonctions
import maths
import matplotlib.pyplot as plt

# region Definition des variables

# - score_moyenne_generations = la moyenne du score pour chaque generations
score_moyenne_generations = []

# - portee_moyenne_generations = la moyenne de la portee pour chaque generations
portee_moyenne_generations = []

# - variance_score_generations = la variance des scores par generations
variance_score_generations = []

# - tnt_moyenne_generations = La moyenne de la tnt par generations
tnt_moyenne_generations = []

individu = {}
# endregion


# Génération des individus de la premiere generation
for i in range(0, config.NB_POPULATION):
    individu[i] = fonctions.creationPopulation()

for j in range(0, config.NB_GEN):
    score_individus = {}
    score_individus_variance = {}
    total_portee_individus = 0
    total_tnt_individus = 0
    total_score_individus = 0

    # Cycle d'évaluation des individus
    for i in range(0, config.NB_POPULATION):
        if i == 0:
            evaluation_individu = fonctions.evaluationIndividu(individu[i])
            score_individus[i] = evaluation_individu[0]
            score_individus_variance[i] = evaluation_individu[0]

            # Le somme total du score, portee et la TNT est sauvegardé pour chaque generation
            total_score_individus = evaluation_individu[0]
            total_portee_individus = evaluation_individu[1]
            total_tnt_individus = evaluation_individu[2]

        else:
            evaluation_individu = fonctions.evaluationIndividu(individu[i])
            score_individus[i] = evaluation_individu[0] + score_individus[i - 1]
            score_individus_variance[i] = evaluation_individu[0]

            # Le somme total du score, portee et la TNT est sauvegardé pour chaque generation
            total_score_individus = total_score_individus + evaluation_individu[0]
            total_portee_individus = total_portee_individus + evaluation_individu[1]
            total_tnt_individus = total_tnt_individus + evaluation_individu[2]

    # Selection des parents avec la méthode RWS
    liste_couples = (fonctions.selectionParent(score_individus, individu))

    # Création des enfants, 2 par couples
    individu = fonctions.creationEnfants(liste_couples)

    # Calcul de la moyenne du score, portee, TNT et de la variance par génération
    score_moyenne_generations.append(total_score_individus / config.NB_POPULATION)
    portee_moyenne_generations.append(total_portee_individus / config.NB_POPULATION)
    tnt_moyenne_generations.append(total_tnt_individus / config.NB_POPULATION)
    variance_score_generations.append(
        (maths.calculVarianceScore(score_individus_variance, score_moyenne_generations[j])) / 1000)

    print("Génération : " + str(j))
    print("Moyenne de la portee de cette generation : " + str(portee_moyenne_generations[j]))

# Generation du graphe
x = range(0, config.NB_GEN)
plt.figure(1)
plt.xlabel('Nb generation')
plt.subplot(221)
plt.title("Score en fonction du nombre de generation")
plt.ylabel('Fitness')
plt.plot(x, score_moyenne_generations)
plt.subplot(222)
plt.title("Variance Fitness en fonction du nombre de génération")
plt.ylabel("variance")
plt.plot(x, variance_score_generations)
plt.subplot(223)
plt.title("Portee en fonction du nombre de generation")
plt.ylabel("Portee en metre")
plt.plot(x, portee_moyenne_generations)
plt.subplot(224)
plt.title("Energie en fonction du nombre de génération")
plt.ylabel("Energie en gramme de TNT")
plt.plot(x, tnt_moyenne_generations)

plt.show()
