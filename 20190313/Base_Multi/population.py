from chromosome import Chromosome
import threading
import time

def get_first(chromosomes, half):
    i = 0
    while i < half:
        chromosomes.append(Chromosome())
        i += 1

def get_second(chromosomes, half):
    i = 0
    while i < half:
        chromosomes.append(Chromosome())
        i += 1

class Population:
    # population of candidate solutions
    def __init__(self, size):
        self._chromosomes = []
        half =  size/2

        first_thread = threading.Thread(target=get_first, args=(self._chromosomes, half))
        second_thread = threading.Thread(target=get_second, args=(self._chromosomes, half))

        first_thread.start()
        second_thread.start()

    def get_chromosomes(self):
        return self._chromosomes

