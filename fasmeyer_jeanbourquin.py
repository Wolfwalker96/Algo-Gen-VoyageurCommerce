"""
Probleme du voyageur
"""

import pygame
from random import randint, getrandbits, shuffle, random
from functools import reduce


cities = list()


class SelectMethod:

    @staticmethod
    def wheel(individuals):
        pass

    @staticmethod
    def elites(individuals):
        return individuals[:20]


class Individual:
    """Individual representation."""
    path = list()

    def __init__(self, path):
        self.path = list(path)

    def __str__(self):
        return f"{self.fitness()} - {', '.join([city.name for city in self.path])}"

    def fitness(self):
        sum = 0
        for j, city in enumerate(self.path):
            sum += distance_between_cities(city, self.path[(j+1) % len(self.path)])
        return sum

    def mutate(self):
        """Mutate once, swap two genes."""
        pos, dist = randint(0, len(self.path)-1), randint(0, len(self.path))
        new_pos = (pos + dist) % len(self.path)
        self.path[new_pos], self.path[pos] = self.path[pos], self.path[new_pos]


class Population:
    size = int()
    mutation_rate = int()
    individuals = list()

    def __init__(self, size, mutation_rate):
        self.size = size
        self.mutation_rate = mutation_rate
        self.init_population()

    def __str__(self):
        return str(self.individuals[0])

    def init_population(self):
        for i in range(0, self.size):
            tmp = list(cities)
            shuffle(tmp)
            self.individuals.append(Individual(tmp))

    def reproduce(self):
        elites = self.select(SelectMethod.elites)
        self.individuals.clear()
        for a, b in zip(range(0, len(elites), 2), range(1, len(elites), 2)):
            self.individuals.append(hybridization(elites[a], elites[b]))
            self.individuals.append(hybridization(elites[b], elites[a]))

    def select(self, func):
        sorted(self.individuals, key=lambda x: x.fitness())
        return func(self.individuals)


class Window:
    import pygame

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
    pos_x = int()
    pos_y = int()
    name = str()

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


def ga_solve(file=None, gui=True, maxtime=0):
    """Algorithm"""
    if file is not None:
        City.load_cities(file)
    else:
        win = Window()
        win.show()

    #print("\n".join([str(city) for city in cities]))
    test = Individual(cities)
    tmp = list(cities)
    shuffle(tmp)
    test2 = Individual(tmp)
    print(test)
    test.mutate()
    print(test)

    print(test2)
    print(hybridization(test, test2))

    pop = Population(100, 0.3)
    pop.reproduce()


if __name__ == "__main__":
    ga_solve(file="data/pb020.txt")
