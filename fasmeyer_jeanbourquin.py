"""
Probleme du voyageur
"""

'''
1. Crossover doesn't work well with big path..
1.1 We can separate cities in area within a 'r' radius.

2. Try other selection algorithms (wheel), ours doesn't work well with big values.

3. ADD dynamic parameter modification?
'''

import pygame
from random import randint, shuffle, random
from functools import reduce
from math import sqrt, pi, e

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
        msg=""
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

        self.screen.fill(0)
        pygame.draw.lines(self.screen, self.city_color, True, [(city.pos_x, city.pos_y) for city in cities])
        text = self.font.render("Un chemin, pas le meilleur!", True, self.font_color)
        textRect = text.get_rect()
        self.screen.blit(text, textRect)
        pygame.display.flip()

        while True:
            event = pygame.event.wait()
            if event.type == KEYDOWN: break


class GA:
    def __init__(self, population_size = 100, mutation_rate = 0.05, elitism = True, tournament_size = 5):
        self.population = Population(population_size)
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.elitism = elitism
        self.tournament_size = tournament_size
        self.chosen_one = self.population.best_chromosome

    def __str__(self):
        return f"{self.population}"

    def mutate(self, chromosome):
        """Mutate the chromosome by swapping.
        Will never swap a gene with itself. (see: position, distance)
        Made to use two 'randint()' only.
        """
        genes_size = len(chromosome.genes)
        for pos in range(0, genes_size):
            # Do we mutate this chromosome?
            if(random() < self.mutation_rate):
                dist = randint(0, genes_size)
                new_pos = (pos + dist) % genes_size
                # Old school switch (not enough space horizontaly).
                temp = chromosome.genes[new_pos]
                chromosome.genes[new_pos] = chromosome.genes[pos]
                chromosome.genes[pos] = temp
                chromosome.update_fitness()

    def crossover(self, a: Chromosome, b: Chromosome):
        '''Explode as the number of cities rise!'''
        fa = True
        fb = True
        # Choose random town, find where it is within a and b.
        n = len(a.genes) # O(1).
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
                    g.insert(0, ax) # O(1).
                    c.remove(ax)    # O(n).
                else:
                    fa = False

            if fb is True:
                if by not in g:
                    g.append(by) # O(1).
                    c.remove(by) # O(n).
                else:
                    fb = False
        if len(g) < n:
            # Add rest of rows at random.
            shuffle(c)  # O(n).
            g.extend(c) # O(k).
        return Chromosome(g)

    def selection(self):
        '''The more chromosomes in the tournament, the more processing
        power will be required.'''
        parents = SelectionMethod.tournament(
            self.population.chromosomes,
            self.tournament_size)
        return parents

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
        if (self.chosen_one.fitness <
            self.population.best_chromosome.fitness):
            # Bad indentation PEP8.
            self.chosen_one = self.population.best_chromosome


class SelectionMethod:

    @staticmethod
    def tournament(chromosomes, tournament_size):
        winners = list()
        # Select 'n' winners.
        for i in range(0, len(chromosomes)):
            challengers = list()
            # Select 'm' challengers.
            for i in range(0, tournament_size):
                index = randint(0, len(chromosomes)-1)
                challengers.append(chromosomes[index])

            winner = max(challengers, key=lambda c : c.fitness)
            winners.append(winner)

        return winners


def path_length(genes : list):
    """Return the length of a path."""
    sum = 0
    for i in range(1, len(genes)):
        sum += sqrt( distance_between_cities(genes[i-1], genes[i]) )
    sum += sqrt( distance_between_cities(genes[0], genes[len(genes)-1]) )
    return sum


def distance_between_cities(a: City, b: City):
    """Returns the squared distance between city a and b."""
    return abs(a.pos_x - b.pos_x)**2+abs(a.pos_y-b.pos_y)**2


def stirling(n):
    """Used to determine the number of solutions."""
    return sqrt(2*pi*n)*(n/e)**n


def ga_solve(file=None, gui=True, max_time=0):
    # Input management.
    global cities
    cities = list()
    if file is not None:
        City.load_cities(file)
    else:
        win = Window()
        win.show()

    # Start AG.
    from time import time
    start_time = time()
    
    if len(cities) <= 50:
        POPULATION_SIZE = 130
        TOURNAMENT_SIZE = int(POPULATION_SIZE*0.50)
        MUTATION_RATE = 0.0053
    else:
        POPULATION_SIZE = 150
        TOURNAMENT_SIZE = int(POPULATION_SIZE*0.40)
        MUTATION_RATE = 0.006


    ga = GA(
        population_size = POPULATION_SIZE,
        mutation_rate = MUTATION_RATE,
        elitism=True,
        tournament_size = TOURNAMENT_SIZE)

    while ((time()-start_time) < max_time) or False:
        ga.run_step()

    r1 = ga.chosen_one.path_length
    r2 = [city.name for city in ga.chosen_one.genes]
    return r1, r2



if __name__ == "__main__":
    from sys import argv
    file = None
    gui = True
    max_time = 0
    for i, arg in enumerate(argv[1:]):
        if arg == "--nogui":
            gui = False
        elif arg == "--maxtime":
            max_time = int(argv[i+2])
        else:
            file = arg

    length, genes = ga_solve(file=file, max_time=max_time, gui=gui)
    print(f"Distance : {int(length)}\nChemin : {', '.join(genes)}")
