from chromosome import Chromosome

class Population:
    # population of candidate solutions
    def __init__(self, size, days, stock_prices):
        self._chromosomes = []
        i = 0
        while i < size:
            self._chromosomes.append(Chromosome(days, stock_prices))
            i += 1

    def get_chromosomes(self):
        return self._chromosomes
