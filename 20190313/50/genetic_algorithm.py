from chromosome import Chromosome
from population import Population

import os
import glob
import random


file_names = [os.path.basename(x) for x in glob.glob('./kospi200/*.csv')]
KOSPI_TICKER = []
count = 0
for file_name in file_names:
    KOSPI_TICKER.append(os.path.splitext(file_name)[0])
    count += 1
    if count >= 50:
        break
# KOSPI_TICKER = ['000070.KS', '000080.KS', '000100.KS', '000120.KS', '000150.KS', '000210.KS', '000240.KS', '000270.KS', '000640.KS', '000660.KS']
# KOSPI_TICKER = ['000070.KS', '000080.KS', '000100.KS', '000120.KS', '000150.KS']
NUM_OF_STOCKS = len(KOSPI_TICKER)

POPULATION_SIZE = 100
STOCK_SELCTION_RATE = 0.1

NUM_OF_ELITE_CHROMOSOMES = 5
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1


class GeneticAlgorithm:

    # selection, crossover, mutation and elitism logic
    @staticmethod
    def evolve(pop):
        # print("EVOLVING")
        return GeneticAlgorithm._mutate_population(GeneticAlgorithm._crossover_population(pop))

    @staticmethod
    def _mutate_population(pop):
        for index in range(NUM_OF_ELITE_CHROMOSOMES, POPULATION_SIZE):
            GeneticAlgorithm._mutate_chromosome(pop.get_chromosomes()[index])
        return pop

    @staticmethod
    def _crossover_population(pop):
        crossover_pop = Population(0)
        for index in range(NUM_OF_ELITE_CHROMOSOMES):
            crossover_pop.get_chromosomes().append(pop.get_chromosomes()[index])
        index = NUM_OF_ELITE_CHROMOSOMES
        while index < POPULATION_SIZE:
            chromosome1 = GeneticAlgorithm._select_tournament_population(pop).get_chromosomes()[0]
            chromosome2 = GeneticAlgorithm._select_tournament_population(pop).get_chromosomes()[0]
            crossover_pop.get_chromosomes().append(GeneticAlgorithm._crossover_chromosomes(chromosome1, chromosome2))
            index += 1
        return crossover_pop

    @staticmethod
    def _mutate_chromosome(chromosome):
        for index in range(NUM_OF_STOCKS):
            if random.random() <= MUTATION_RATE:
                if random.random() <= STOCK_SELCTION_RATE:
                    chromosome.get_genes()[index] = 1
                else:
                    chromosome.get_genes()[index] = 0
        return chromosome

    @staticmethod
    def _crossover_chromosomes(chromosome1, chromosome2):
        crossover_chromosome = Chromosome()
        for index in range(NUM_OF_STOCKS):
            if random.random() <= STOCK_SELCTION_RATE:
                crossover_chromosome.get_genes()[index] = chromosome1.get_genes()[index]
            else:
                crossover_chromosome.get_genes()[index] = chromosome2.get_genes()[index]
        return crossover_chromosome

    @staticmethod
    def _select_tournament_population(pop):
        tournament_pop = Population(0)
        index = 0
        while index < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_chromosomes().append(pop.get_chromosomes()[random.randrange(0, POPULATION_SIZE)])
            index += 1

        tournament_pop.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)

        return  tournament_pop
