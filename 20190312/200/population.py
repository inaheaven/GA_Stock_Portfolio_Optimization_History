from chromosome import Chromosome
from threading import *
from time import sleep

class Population:
    # population of candidate solutions
    def __init__(self, size):
        self._chromosomes = []
        i = 0
        while i < size:
            self._chromosomes.append(Chromosome())
            i += 1

    def get_chromosomes(self):
        return self._chromosomes

