"""
Probleme du voyageur
"""

import pygame
from random import randint, shuffle, random, uniform
from math import sqrt
from heapq import nlargest, nsmallest


class City:

    def __init__(self, pos_x=0, pos_y=0, name=""):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.name = name

    def __str__(self):
        return f"{self.name} ({self.pos_x}, {self.pos_y})"

    @staticmethod
    def load_cities(filename):
        with open(filename) as file:
            for line in file:
                name, pos_x, pos_y = line.split()
                cities.append(City(int(pos_x), int(pos_y), name))


class Chromosome:
    """Use genes to represent the path. Each gene is a city."""
    def __init__(self, genes):
        self.genes = list(genes)
        self.fit = None

    def __str__(self):
        return f"{self.fitness} ({', '.join([city.name for city in self.genes])})"

    def update_fitness(self):
        """Update fitness.
        Should not be used for anything else than UI or debug purposes.
        A chromosome fitness is not supposed to change after its creation
        (crossover + mutation).
        """
        self.fit = None

    @property
    def fitness(self):
        """Return a fitness based on the squared path length."""
        if self.fit is None:
            self.fit = 1/path_length(self.genes)

        return self.fit

    @property
    def path_length(self):
        """Return the path length."""
        return path_length(self.genes)


class Population:

    def __init__(self, size):
        self.size = size
        self.chromosomes = list()
        self.init_population()

    def __str__(self):
        msg = ""
        for chromosome in self.chromosomes:
            msg += f"{chromosome}\n"
        msg += f"Avg_fitness: {self.avg_fitness}\n"
        msg += f"\nBest chromosome: \nFitness: {self.best_chromosome}"
        msg += f"\nLength: {path_length(self.best_chromosome.genes)}\n"

        return msg

    def init_population(self):
        for i in range(0, self.size):
            tmp = list(cities)
            shuffle(tmp)
            self.chromosomes.append(Chromosome(tmp))

    @property
    def best_chromosome(self):
        """Return the best chromosome."""
        return max(self.chromosomes, key=lambda c : c.fitness)

    @property
    def avg_fitness(self):
        cs = self.chromosomes
        sum = 0
        for c in cs:
            sum += c.fitness
        return sum / len(cs)


class Window:

    screen_x = 500
    screen_y = 500

    city_color = [10, 10, 200]  # blue
    city_radius = 3

    font_color = [255, 255, 255]  # white

    def draw(self, positions):
        self.screen.fill(0)
        for pos in positions:
            pygame.draw.circle(self.screen, self.city_color, (pos.pos_x, pos.pos_y), self.city_radius)
        text = self.font.render("Nombre: %i" % len(positions), True, self.font_color)
        text_rect = text.get_rect()
        self.screen.blit(text, text_rect)
        pygame.display.flip()

    def show(self):
        from pygame.locals import KEYDOWN, QUIT, MOUSEBUTTONDOWN, K_RETURN, K_ESCAPE
        pygame.init()
        self.window = pygame.display.set_mode((self.screen_x, self.screen_y))
        pygame.display.set_caption('Exemple')
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        self.draw(cities)

        collecting = True

        while collecting:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN and event.key == K_RETURN:
                    collecting = False
                elif event.type == MOUSEBUTTONDOWN:
                    cities.append(City(name=f"v{len(cities)}",
                                       pos_x=pygame.mouse.get_pos()[0],
                                       pos_y=pygame.mouse.get_pos()[1]))
                    self.draw(cities)

    def draw_path(self, cities):
        self.screen.fill(0)
        pygame.draw.lines(self.screen, self.city_color, True, [(city.pos_x, city.pos_y) for city in cities])
        text = self.font.render("Un chemin, pas le meilleur!", True, self.font_color)
        textRect = text.get_rect()
        self.screen.blit(text, textRect)
        pygame.display.flip()


class GA:
    def __init__(self,
                 population_size=100,
                 mutation_rate=0.05,
                 elitism=True,
                 roulette_ratio=0.7,
                 tournament_ratio=0.2,
                 elitism_ratio=0.1,
                 tournament_size=5):
        self.population = Population(population_size)
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        # Put the chosen one back within the population. Chosen one can be old.
        self.elitism = elitism
        self.roulette_ratio = roulette_ratio
        self.tournament_ratio = tournament_ratio
        self.elitism_ratio = elitism_ratio
        self.tournament_size = tournament_size
        self.chosen_one = self.population.best_chromosome

    def __str__(self):
        return f"{self.population}"

    def mutate(self, chromosome):
        """Mutate the chromosome by swapping."""
        genes_size = len(chromosome.genes)
        ''' Reduce the number of mutation checks by a factor of 20.
        Rise the mutation rate and get the same result for processing pow.
        '''
        max_mutations = int(genes_size*0.05)+2
        start = randint(0, max_mutations-1)
        for pos in range(start, genes_size, max_mutations):
            # Do we mutate this chromosome?
            if random() < self.mutation_rate:
                dist = randint(0, genes_size)
                new_pos = (pos + dist) % genes_size
                # Old school swap (not enough space horizontaly).
                temp = chromosome.genes[new_pos]
                chromosome.genes[new_pos] = chromosome.genes[pos]
                chromosome.genes[pos] = temp
                chromosome.update_fitness()

    def crossover(self, a: Chromosome, b: Chromosome):
        '''Explode as the number of cities rise!'''
        fa = True
        fb = True
        # Choose random town, find where it is within a and b.
        n = len(a.genes)  # O(1).
        start_town = a.genes[randint(0, n-1)]
        x = a.genes.index(start_town)
        y = b.genes.index(start_town)
        g = list()
        c = list(a.genes)

        while fa is True and fb is True:
            x = (x - 1) % n
            y = (y + 1) % n
            ax = a.genes[x]
            by = a.genes[y]
            if fa is True:
                if ax not in g:
                    g.insert(0, ax)  # O(1).
                    c.remove(ax)     # O(n).
                else:
                    fa = False

            if fb is True:
                if by not in g:
                    g.append(by)  # O(1).
                    c.remove(by)  # O(n).
                else:
                    fb = False
        if len(g) < n:
            # Add rest of rows at random.
            shuffle(c)   # O(n).
            g.extend(c)  # O(k).
        return Chromosome(g)

    def selection(self):
        winners = list()
        chromosomes = self.population.chromosomes

        # Select parents for the new population.
        nb_roulette = int(self.population_size * self.roulette_ratio)
        nb_elitism = int(self.population_size * self.elitism_ratio)
        nb_tournament = int(self.population_size * self.tournament_ratio)

        total = nb_roulette + nb_elitism + nb_tournament
        if(total < self.population_size):
            nb_roulette += self.population_size - total

        winners1 = SelectionMethod.elitist(chromosomes, nb_elitism)
        winners2 = SelectionMethod.roulette(chromosomes, nb_roulette)
        winners3 = SelectionMethod.tournament(
            chromosomes, nb_tournament, self.tournament_size)

        if self.population_size != len(chromosomes):
            print(f"ERROR! POPULATION COUNT OUT OF RANGE!")
            print(f"pop: {len(self.population.chromosomes)}")
            print(f"elit: {len(winners1)}")
            print(f"roulette: {len(winners2)}")
            print(f"tournament: {len(winners3)}")

        winners.extend(winners1)
        winners.extend(winners2)
        winners.extend(winners3)
        return winners

    def run_step(self):
        """Run one step, create a new generation from the parents."""
        # Selection.
        parents = self.selection()
        if self.elitism is True:
            parents[0] = Chromosome(self.chosen_one.genes)

        # Crossover.
        new_population = list()
        for a, b in zip(range(0, len(parents), 2), range(1, len(parents), 2)):
            new_population.append(self.crossover(parents[a], parents[b]))
            new_population.append(self.crossover(parents[b], parents[a]))

        # Mutation.
        for child in new_population:
            self.mutate(child)

        self.population.chromosomes = new_population

        # Evaluation (always keep the best one)
        if self.chosen_one.fitness < self.population.best_chromosome.fitness:
            # Bad indentation PEP8.
            self.chosen_one = self.population.best_chromosome


class SelectionMethod:

    @staticmethod
    def tournament(chromosomes, nb_winners, tournament_size = 2):
        """Classical tournament selection."""
        winners = list()
        if nb_winners == 0:
            return winners

        nb_challengers = int(nb_winners * tournament_size)
        if nb_challengers <= 1:
            nb_challengers = 2

        # Select 'n' winners (parents).
        for i in range(0, nb_winners):
            challengers = list()
            # Select 'm' challengers.
            for i in range(0, nb_challengers):
                index = randint(0, len(chromosomes)-1)
                challengers.append(chromosomes[index])

            winner = max(challengers, key=lambda c: c.fitness)
            winners.append(winner)

        return winners

    @staticmethod
    def roulette(chromosomes, nb_winners):
        """Roulette selection."""
        winners = list()
        if nb_winners == 0:
            return winners

        sum = 0
        for c in chromosomes:
            sum += c.fitness

        ratio = 1/sum
        for i in range(0, nb_winners):
            cumulated = 0
            rdm_select = random()
            for c in chromosomes:
                threshold = cumulated + (c.fitness*ratio)

                if rdm_select <= threshold:
                    winners.append(c)
                    break
                cumulated = threshold
        return winners

    @staticmethod
    def elitist(chromosomes, nb_winners):
        """Pure elitism."""
        winners = list()
        if nb_winners == 0:
            return winners

        winners = nlargest(
            nb_winners,
            chromosomes,
            key=lambda c : c.fitness)

        return winners


def path_length(genes: list):
    """Return the length of a path."""
    sum = 0
    for i in range(1, len(genes)):
        sum += sqrt(distance_between_cities(genes[i-1], genes[i]))

    sum += sqrt(distance_between_cities(genes[0], genes[len(genes)-1]))
    return sum


def distance_between_cities(a: City, b: City):
    """Returns the squared distance between city a and b."""
    return abs(a.pos_x - b.pos_x)**2+abs(a.pos_y-b.pos_y)**2


def ga_solve(file=None, gui=True, max_time=0):
    # Input management.
    global cities
    cities = list()

    if file is not None:
        City.load_cities(file)
    else:
        win = Window()
        win.show()
    if gui:
        win = Window()
        win.show()

    from time import time
    start_time = time()

    # Configuration parameters.
    if len(cities) <= 10:
        POPULATION_SIZE = 10
        MUTATION_RATE = 0.008
        ROULETTE_RATIO=0.9
        TOURNAMENT_RATIO=0
        ELITISM_RATIO=0.2
        TOURNAMENT_SIZE=5
    elif len(cities) <= 50:
        POPULATION_SIZE = 230
        MUTATION_RATE = 0.03
        ROULETTE_RATIO=0.7
        TOURNAMENT_RATIO=0.2
        ELITISM_RATIO=0.1
        TOURNAMENT_SIZE=5
    else:
        POPULATION_SIZE = 100
        MUTATION_RATE = 0.012
        ROULETTE_RATIO=0.7
        TOURNAMENT_RATIO=0.2
        ELITISM_RATIO=0.1
        TOURNAMENT_SIZE=5
        '''
    POPULATION_SIZE = 100
    MUTATION_RATE = 0.03
    ROULETTE_RATIO=0.8
    TOURNAMENT_RATIO=0.1
    ELITISM_RATIO=0.1
    TOURNAMENT_SIZE=100
    '''

    ga = GA(
        population_size=POPULATION_SIZE,
        mutation_rate=MUTATION_RATE,
        elitism=True,
        tournament_ratio=TOURNAMENT_RATIO,
        elitism_ratio=ELITISM_RATIO,
        roulette_ratio=ROULETTE_RATIO,
        tournament_size=TOURNAMENT_SIZE
        )

    # Only by tournament.
    ga.process = 0

    old_chosen_one = list()
    continue_run = True
    # Algorithm main loop.
    while ((time()-start_time) < max_time or max_time == 0) and continue_run:
        ga.run_step()
        old_chosen_one.append(ga.chosen_one.fitness)
        if gui:
            win.draw_path(ga.chosen_one.genes)
        if max_time == 0:
            if old_chosen_one[-15:-1].count(old_chosen_one[-1]) >= 5:
                continue_run = False

    # Return results.
    r1 = ga.chosen_one.path_length
    r2 = [city.name for city in ga.chosen_one.genes]
    return r1, r2


if __name__ == "__main__":
    from sys import argv
    file = None
    gui = True
    max_time = 0
    shown_args = list()
    for i, arg in enumerate(argv[1:]):
        if arg not in shown_args:
            if arg == "--nogui":
                gui = False
            elif arg == "--maxtime":
                max_time = int(argv[i+2])
                shown_args.append(argv[i + 2])
            else:
                file = arg
            shown_args.append(arg)

    length, genes = ga_solve(file=file, max_time=max_time, gui=gui)
    print(f"Distance : {int(length)}\nChemin : {', '.join(genes)}")
