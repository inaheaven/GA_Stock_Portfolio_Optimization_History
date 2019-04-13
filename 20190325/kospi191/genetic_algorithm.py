from settings import *
from chromosome import Chromosome
from population import Population

import random


class GeneticAlgorithm:
    # selection, crossover, mutation and elitism logic
    @staticmethod
    def evolve(pop, days, stock_prices, population_size):
        return GeneticAlgorithm._mutate_population(GeneticAlgorithm._crossover_population(pop, days, stock_prices, population_size), population_size)

    @staticmethod
    def _mutate_population(pop, population_size):
        for index in range(NUM_OF_ELITE_CHROMOSOMES, population_size):
            GeneticAlgorithm._mutate_chromosome(pop.get_chromosomes()[index])
        return pop

    @staticmethod
    def _crossover_population(pop, days, stock_prices, population_size):
        crossover_pop = Population(0, days, stock_prices)
        for index in range(NUM_OF_ELITE_CHROMOSOMES):
            crossover_pop.get_chromosomes().append(pop.get_chromosomes()[index])
        index = NUM_OF_ELITE_CHROMOSOMES
        while index < population_size:
            chromosome1 = GeneticAlgorithm._select_tournament_population(pop, days, stock_prices, population_size).get_chromosomes()[0]
            chromosome2 = GeneticAlgorithm._select_tournament_population(pop, days, stock_prices, population_size).get_chromosomes()[1]
            crossover_pop.get_chromosomes().append(GeneticAlgorithm._crossover_chromosomes(chromosome1, chromosome2, days, stock_prices))
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
    def _crossover_chromosomes(chromosome1, chromosome2, days, stock_prices):
        crossover_chromosome = Chromosome(days, stock_prices)
        for index in range(NUM_OF_STOCKS):
            if random.random() <= STOCK_SELCTION_RATE:
                crossover_chromosome.get_genes()[index] = chromosome1.get_genes()[index]
            else:
                crossover_chromosome.get_genes()[index] = chromosome2.get_genes()[index]
        return crossover_chromosome

    @staticmethod
    def _select_tournament_population(pop, days, stock_prices, population_size):
        tournament_pop = Population(0, days, stock_prices)
        index = 0
        while index < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_chromosomes().append(pop.get_chromosomes()[random.randrange(0, population_size)])
            index += 1
        tournament_pop.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
        return  tournament_pop
