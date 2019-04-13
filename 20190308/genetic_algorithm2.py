from chromosome import Chromosome
from population import Population
import random

POPULATION_SIZE = 8
NUM_OF_ELITE_CHROMOSOMES = 1
TOURNAMENT_SELECTION_SIZE = 4
MUTATION_RATE = 0.25


class GeneticAlgorithm:

    # selection, crossover, mutation and elitism logic
    @staticmethod
    def evolve(pop):
        print("evolve")
        return GeneticAlgorithm._mutate_population(GeneticAlgorithm._crossover_population(pop))

    @staticmethod
    def _mutate_population(pop):
        for i in range(NUM_OF_ELITE_CHROMOSOMES, POPULATION_SIZE):
            GeneticAlgorithm._mutate_chromosome(pop.get_chromosomes()[0])
        return pop

    @staticmethod
    def _crossover_population(pop):
        crossover_pop = Population(0)
        for i in range(NUM_OF_ELITE_CHROMOSOMES):
            crossover_pop.get_chromosomes().append(pop.get_chromosomes()[0])
            index = 0
            while index < TOURNAMENT_SELECTION_SIZE:
                chromosome1 = GeneticAlgorithm._select_tournament_population(pop).get_chromosomes()[0]
                chromosome2 = GeneticAlgorithm._select_tournament_population(pop).get_chromosomes()[0]
                # print("chromosome1", GeneticAlgorithm._select_tournament_population(pop).get_chromosomes()[0])
                # print("chromosome2", GeneticAlgorithm._select_tournament_population(pop).get_chromosomes()[1])
                # print("chromosome3", GeneticAlgorithm._select_tournament_population(pop).get_chromosomes()[2])
                # print("chromosome4", GeneticAlgorithm._select_tournament_population(pop).get_chromosomes()[3])
                crossover_pop.get_chromosomes().append(GeneticAlgorithm._crossover_chromosomes(chromosome1, chromosome2))
                index += 1
        return crossover_pop

    @staticmethod
    def _crossover_chromosomes(chromosome1, chromosome2):
        crossover_chrom = Chromosome()
        for i in range(len(crossover_chrom.get_genes())):
            if random.random() >= 0.5:
                crossover_chrom.get_genes()[i] = chromosome1.get_genes()[i]
            else:
                crossover_chrom.get_genes()[i] = chromosome2.get_genes()[i]
        return crossover_chrom

    @staticmethod
    def _mutate_chromosome(chromosome):
        for i in range(len(chromosome.get_genes())):
           if random.random() < MUTATION_RATE:
               if random.random() < 0.5:
                   chromosome.get_genes()[i] = 1
               else:
                   chromosome.get_genes()[i] = 0

    @staticmethod
    def _select_tournament_population(pop):
        tournament_pop = Population(0)
        i = 0
        while i< TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_chromosomes().append(pop.get_chromosomes()[random.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse=True)
        return  tournament_pop
