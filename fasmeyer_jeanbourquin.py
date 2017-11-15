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
    # print("\n".join([str(city) for city in cities]))


if __name__ == "__main__":
    ga_solve(file="data/pb005.txt")
