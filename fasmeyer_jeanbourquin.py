"""
Probleme du voyageur
"""

import pygame
from random import randint, getrandbits, shuffle


cities = list()


class Individual:
    """Individual representation."""
    path = list()

    def __init__(self, path):
        self.path = path

    def fitness(self):
        return reduce(distance_between_cities, self.path)

    def mutate(self):
        """Mutate once, swap two genes."""
        pos, dist = randint(0, len(path)), randint(0, len(path))
        newpos = (pos + dist) % len(path)
        path[newpos], path[pos] = path[pos], path[newpos]


class Population:
    size = int()
    mutation_rate = int()
    individuals = list()

    def __init__(self, size, mutation_rate):
        self.size = size
        self.mutation_rate = mutation_rate

    def init_population(self):
        for i in range(0, size):
            Individuals.append(Individual(cities.shuffle))

    def reproduce(self):
        elites = self.select()
        self.individuals.clear()
        for a, b in (range(0, elites.length(), 2), range(1, elites.length(), 2)):
            self.individuals.append(hybridization(elites[a], elites[b]))
            self.individuals.append(hybridization(elites[b], elites[a]))

    def select(self, func):
        return func(self.individuals)


class Window:
    import pygame

    screen_x = 500
    screen_y = 500

    city_color = [10, 10, 200]  # blue
    city_radius = 3

    font_color = [255, 255, 255]  # white

    pygame.init()
    window = pygame.display.set_mode((screen_x, screen_y))
    pygame.display.set_caption('Exemple')
    screen = pygame.display.get_surface()
    font = pygame.font.Font(None, 30)

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
        import sys
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
        pygame.draw.lines(self.screen, self.city_color, True, cities)
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
                cities.append(City(pos_x, pos_y, name))


def distance_between_cities(a: City, b: City):
    """Returns the distance squared between cites a and b."""
    return abs(a.pos_x - b.pos_x) + abs(a.pos_y - b.pos_y)


def hybridization(a: Individual, b: Individual):
    return a


def ga_solve(file=None, gui=True, maxtime=0):
    """Algorithm"""
    if file is not None:
        City.load_cities(file)
    else:
        win = Window()
        win.show()

    print("\n".join([str(city) for city in cities]))


if __name__ == "__main__":
    ga_solve(file=None)
