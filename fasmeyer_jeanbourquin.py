"""
Probleme du voyageur
"""

import pygame
from random import randint, shuffle, random
from math import sqrt


class SelectMethod:

    @staticmethod
    def tournament(individuals):
        TOURNAMENT_SIZE = 5
        winners = list()
        number_of_parents = len(individuals)
        winners = list()
        for i in range(0, number_of_parents):
            challengers = list()
            for i in range(0, TOURNAMENT_SIZE):
                index = randint(0, len(individuals)-1)
                challengers.append(individuals[index])

            sorted(challengers, key=lambda c: c.fitness)
            winners.append(challengers[0])

        return winners

    @staticmethod
    def elites(individuals):
        number_of_parents = len(individuals)
        return individuals[:number_of_parents]


class Individual:
    """Individual representation."""

    def __init__(self, path):
        self.path = list(path)

    def __str__(self):
        return f"{self.fitness()} - {', '.join([city.name for city in self.path])}"

    @property
    def fitness(self):
        sum = 0
        for j, city in enumerate(self.path):
            sum += sqrt(distance_between_cities(city, self.path[(j+1) % len(self.path)]))
        return sum

    def mutate(self):
        """Mutate once, swap two genes."""
        pos, dist = randint(0, len(self.path)-1), randint(0, len(self.path))
        new_pos = (pos + dist) % len(self.path)
        self.path[new_pos], self.path[pos] = self.path[pos], self.path[new_pos]


class Population:

    def __init__(self, size, mutation_rate):
        self.size = size
        self.mutation_rate = mutation_rate
        self.individuals = list()
        self.init_population()

    def __str__(self):
        return str(self.individuals[0])

    def init_population(self):
        for i in range(0, self.size):
            tmp = list(cities)
            shuffle(tmp)
            self.individuals.append(Individual(tmp))

    def reproduce(self):
        # Select the old population to reproduce.
        elites = self.select(SelectMethod.tournament)
        # Create a new population
        self.individuals.clear()
        for a, b in zip(range(0, len(elites), 2), range(1, len(elites), 2)):
            self.individuals.append(hybridization(elites[a], elites[b]))
            self.individuals.append(hybridization(elites[b], elites[a]))

        # Mutate new population.
        for new_born in self.individuals:
            self.mutate(new_born)

        # Return the best of the old population (for records).
        return elites[0]

    def select(self, func):
        sorted(self.individuals, key=lambda x: x.fitness)
        return func(self.individuals)

    def mutate(self, individual):
        '''
        Try to mutate every genes(cities) by swapping.
        Will never swap the same city twice (see: position, distance)
        Made to use two randoms instead of three.
        '''
        path_size = len(individual.path)
        for pos in range(0, path_size):
            # Do we mutate this gene?
            if(random() < self.mutation_rate):
                dist = randint(0, path_size)
                new_pos = (pos + dist) % path_size
                temp = individual.path[new_pos]
                individual.path[new_pos] = individual.path[pos]
                individual.path[pos] = temp


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


class City:
    """City representation"""

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


def distance_between_cities(a: City, b: City):
    """Returns the distance squared between cites a and b."""
    return abs(a.pos_x - b.pos_x)**2+abs(a.pos_y-b.pos_y)**2


def hybridization(a: Individual, b: Individual):
    fa = True
    fb = True
    # Choose random town.
    n = len(a.path)
    start_town = a.path[randint(0, n-1)]
    # Find where start_town is in x.
    x = a.path.index(start_town)
    # Find where start_town is in y.
    y = b.path.index(start_town)
    g = list()
    # Copy of all towns.
    c = list(a.path)

    while fa is True and fb is True:
        x = (x - 1) % n
        y = (y + 1) % n
        ax = a.path[x]
        by = a.path[y]
        if fa is True:
            if ax not in g:
                g.insert(0, ax)
                c.remove(ax)
            else:
                fa = False

        if fb is True:
            if by not in g:
                g.append(by)
                c.remove(by)
            else:
                fb = False
    if len(g) < n:
        # Add rest of rows at random.
        shuffle(c)
        g.extend(c)
    return Individual(g)


def ga_solve(file=None, gui=True, max_time=0):
    """Algorithm"""
    global cities
    cities = list()
    if file is not None:
        City.load_cities(file)
    else:
        win = Window()
        win.show()

    from time import time
    start_time = time()
    pop = Population(100, 0.1)
    last_elites = list()
    while (((time()-start_time) < max_time) and max_time > 0) or False:
        last_elites.append(pop.reproduce())
    sorted(last_elites, key=lambda c: c.fitness)
    return last_elites[0].fitness, [city.name for city in last_elites[0].path]


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

    length, path = ga_solve(file=file, max_time=max_time, gui=gui)
    print(f"Distance : {int(length)}\nChemin : {', '.join(path)}")
