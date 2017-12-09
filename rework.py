"""
Probleme du voyageur
"""

import pygame
from random import randint, shuffle, random
from math import sqrt

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


class Gene:

    def __init__(self, path):
        self.path = list(path)
        self.fit = None

    def __str__(self):
        return f"{self.fitness} ({', '.join([city.name for city in self.path])})"
        #return f"{[city.name for city in self.path]}"

    @property
    def fitness(self):
        """Return a fitness based on the squared path length."""
        if self.fit is None:
            sum = 0
            for i in range(1, len(self.path)):
                sum += distance_between_cities(self.path[i-1], self.path[i])

            self.fit = 1/sum
            return 1/sum

        else:
            return self.fit


class Population:

    def __init__(self, size):
        self.size = size
        self.genes = list()
        self.init_population()

    def __str__(self):
        return str(self.genes[0])

    def init_population(self):
        for i in range(0, self.size):
            tmp = list(cities)
            shuffle(tmp)
            self.genes.append(Gene(tmp))


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

# TO TEST.
def path_length(path : list):
    """Return the length of a path."""
    sum = 0
    for i in range(1, len(path)):
        sum += sqrt( distance_between_cities(path[i-1], path[i]) )
    return sum

# TO TEST.
def distance_between_cities(a: City, b: City):
    """Returns the squared distance between city a and b."""
    return abs(a.pos_x - b.pos_x)**2+abs(a.pos_y-b.pos_y)**2

# TO OPTIMIZE (c.remove is bad)
def crossover(a: Gene, b: Gene):
    fa = True
    fb = True
    # Choose random town, find where it is within a and b.
    n = len(a.path)
    start_town = a.path[randint(0, n-1)]
    x = a.path.index(start_town)
    y = b.path.index(start_town)
    g = list()
    c = list(a.path)

    while fa is True and fb is True:
        x = (x - 1) % n
        y = (y + 1) % n
        ax = a.path[x]
        by = a.path[y]
        if fa is True:
            if ax not in g:
                g.insert(0, ax)
                c.remove(ax) # Too slow!
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

    global cities
    cities = list()
    if file is not None:
        City.load_cities(file)
    else:
        win = Window()
        win.show()

    from time import time
    start_time = time()
    population = Population(1000)

    best_genes = list()
    while ((time()-start_time) < max_time) or False:
        # loop once the GA and get the best of this generation
        pass
    #sorted(best_genes, key=lambda c: c.fitness)
    #return best_genes[0].fitness, [city.name for city in best_genes[0].path]

    # Testing
    a = population.genes
    b = max(a, key=lambda g : g.fitness)
    for gene in a:
        print(gene)
    print(path_length(b.path))

    return None, None


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
    #print(f"Distance : {int(length)}\nChemin : {', '.join(path)}")
