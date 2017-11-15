'''
Probleme du voyageur
'''

import pygame


class Individual:
    '''Individual representation.'''
    path = list()

    def __init__(self, path):
        self.path = path

    def fitness(self):
        distance = 0
        for city in self.path:
            pass
        return distance

    def mutate(self):
        pass


class Population:
    size = int()
    mutation_rate = int()
    individuals = list()

    def __init__(self, size, mutation_rate):
        self.size = size
        self.mutation_rate = mutation_rate

    def reproduce(self):
        elites = self.select()
        self.individuals.clear()
        for a, b in (range(0, elites.length(), 2), range(1, elites.length(), 2)):
            self.individuals.append(hybridization(elites[a], elites[b]))
            self.individuals.append(hybridization(elites[b], elites[a]))

    def select(self, func):
        return func(self.individuals)


class City:
    '''City representation'''
    pos_x = int()
    pos_y = int()

    def __init__(self, pos_x=0, pos_y=0):
        self.pos_x = pos_x
        self.pos_y = pos_y


def hybridization(a: Individual, b: Individual) -> Individual:
    return a


def ga_solve(file=None, gui=True, maxtime=0):
    '''Algorithm'''
    population = Population(1, 0.5)


if __name__ == "__main__":
    ga_solve()
