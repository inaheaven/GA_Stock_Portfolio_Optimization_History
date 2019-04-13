from population import Population
from genetic_algorithm import GeneticAlgorithm

POPULATION_SIZE = 100
GENERATION_SIZE = 200

def _print_population(pop, gen_number):
    print("\n----------------------------------------------")
    print("generation #", gen_number, "| Fittest chromosome fitness:", pop.get_chromosomes()[0].get_fitness())
    print("----------------------------------------------")
    i = 0
    for x in pop.get_chromosomes():
        print("chromosome # ", i, ":", x,  "| Fitness: ", x.get_fitness())
        i += 1


population = Population(POPULATION_SIZE)
population.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse=True)
_print_population(population, 0)
generation_number = 1
while generation_number < GENERATION_SIZE:
    population = GeneticAlgorithm.evolve(population)
    population.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse=True)
    _print_population(population, generation_number)
    generation_number += 1

