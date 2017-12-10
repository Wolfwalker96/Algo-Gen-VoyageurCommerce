Algortihme Génétique - Problème du voyageur de commerce
=======================================================

Classes
-------

### city(gene)
* **pos_x**	Position en x.
* **pos_y**	Position en y.
* **name**	Nom de la ville.

* **load_cities(filename)**
    Charge toutes les villes contenues dans le fichier txt donné.

### Chromosome
* **genes**	Liste de viles composant la solution.

* **fitness()**
	Retourne la valeur de fitness du chromosome.
	Le plus grand, le meilleur est la solution.
* **path_length()**
	Retourne la distance réelle de la solution.

### Population
* **size**	Taille de la population. 
	
* **best_chromosome()**
		Donne le meilleur individu (fitness).
* **avg_fitness**
		Donne la valeur de fitness moyenne.

### GA(algorithm génétique)
Cet algorithme est conçu de manière à ce que l'on puisse modifier les
paramètres en cours d'exécution. L'on peut modifier la taille de la
population, le taux de mutation, le tournament_ratio. un valeur process
est toutes spécialement prévu à cet effet. la valeur de 0 à 100% permet
d'indiquer à l'algorithme le temps restant avant qu'il ne doive se
terminer, permettant par exemple d'augmenter l'élitisme avant la fin
du temps imparti.

* **population_size = 100** Taille de la population.
* **mutation_rate = 0.05** Taux de mutation pour chaques gènes.
* **elitism = True** Copy le meilleur Chromosome dans la population.
* **tournament_ratio = 0.5** % de la population prenant part au tournois.
* **process** % jusqu'à la fin de l'itéaration.	

### Mutation(chromosome)
Swap deux genes d'un chromosome.
* **Selection()** 
	Sélection les chromosomes utilsé pour créer la nouvelle population.
* **crossover(a: Chromosome, b: Chromosome)**
	Mélange les gènes de deux chromosomes.
* **Run_step()**
	Réalise un cycle, une nouvelle génération remplace l'ancienne.
		

### SelectionMethod
Ensemble de méthodes de sélection.
* **roulette(chromosomes)** 
	Méthode simple de sélection. Peu efficace, léger en ressources, peu élitiste
* **turnament(chromosomes, turnament_rate)** 
		Méthode très élitiste, devient TRES lourde le plus vous y ajoutez de 'challengers'.

Beaucoup de combinaisons ont été essayés mais il s'est avèré qu'un fort élitisme semble
être l'une des meilleurs solutions à notre probème. la fonction de sélection 'turnament',
utilisé pour renforcer l'élitisme, est relativemetn lourde et pourait être modifiée.
O(n\*c) avec 'n' nombre de sélections (taill population) et 'c' nombre de challengers,
'c' généralement égale à n\*1/2 (1/2 taille de la population). Ce chiffre est stupidement
grand... autant utiliser une fonction élitiste PUIS sélectionner le reste par tournois de
5 à 7 chromosomes/challengers.

L'on notera que le corrover consome beaucoup de ressources avec l'augmantation du nombre
de villes. O(n*g) avec 'n', nombre de croisements et 'g' taille des gènes. Ce facteur 
est très limitant. il serait intéressant d'implémenter un fonction de croisement par 'cluster',
zones définies arbitrairement, diminuant drastiquement 'b'.

Résultats obtenus avec PVC_Tester
---------------------------------
data\pb005.txt (1s);time: 1.001699447631836, maxtime: 1, tolerance: 1.05
903; parfait!

data\pb010.txt (5s);time: 5.001549482345581, maxtime: 5, tolerance: 5.25
1490; parfait!

data\pb010.txt (10s);time: 10.000122785568237, maxtime: 10, tolerance: 10.5
1490; parfait!

data\pb050.txt (30s);time: 30.036350965499878, maxtime: 30, tolerance: 31.5
3923; ok!

data\pb050.txt (60s);time: 60.03469133377075, maxtime: 60, tolerance: 63.0
3231; ok!

data\pb100.txt (20s);time: 20.030221939086914, maxtime: 20, tolerance: 21.0
8665; mauvais!

data\pb100.txt (90s);time: 90.03399991989136, maxtime: 90, tolerance: 94.5
6836; mauvais!

L'on remarquera que notre algorithme n'arrive que très difficilement à trouver de
nouvelles solutions (minimum local), l'algorithme de sélection ne laisse que peu 
de place à la diversitée tandis que le crossover est lourd et limite la taille de la
population.

Nous avons essayé de règler le problème en mélangeant les algorithmes de sélection,
modifier dynamiquement les paramètres de mutation, sélection, taille de la population,
etc... en fonction du 100% (temps restant) avan la fin ou à l'aide de la dérivée. Rien n'y
fait. Il va falloir améliorer le crossover (très lourd) ou modifier la fonction
de sélection. La mutation quand à elle pourait être un peu plus légère en ne faisant
qu'un certain nombre de modifications par cycle.

En simple
---------
1. Le crossover nous rend la tâche proprotionellement plus dur en fonciton du nb de ville
et de challengers(chromosomes)
2. Le turnament() fait des actions inutiles ou redondantes et est très lourd étrangement
    il marche le mieud quand il peut utiliser 50% de la population comme challengers... horreur!
    Autant le remplacer par une fonciton élitiste puis l'utiliser sur le survivants par groupes
    de 5 à 7.
3. La mutation d'ordre O(2g) avec 'g' étant le nombre de gènes, devrait être simplifiée.
