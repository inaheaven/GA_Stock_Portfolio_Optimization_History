from population import Population
from genetic_algorithm import GeneticAlgorithm

POPULATION_SIZE = 100
GENERATION_SIZE = 200

def _print_population(pop, gen_number):
    num_of_stocks = len(pop.get_chromosomes()[0].get_genes())
    print("\n----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("generation #", gen_number, " - ", pop.get_chromosomes()[0].get_genes(), " | Fittest chromosome fitness:", pop.get_chromosomes()[0].get_fitness())
    print("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")
    print("TOTAL # (", num_of_stocks, ") :", end="")
    for num in range(num_of_stocks):
        stock_num = (num+1) % 10
        print(" ", stock_num, end="")
    print()
    index = 0
    for chromosome in pop.get_chromosomes():
        print("chromosome # ", index, ":", chromosome,  "| Fitness: ", chromosome.get_fitness())
        index += 1


population = Population(POPULATION_SIZE)
population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
_print_population(population, 0)
generation_number = 1
while generation_number < GENERATION_SIZE:
    population = GeneticAlgorithm.evolve(population)
    population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
    _print_population(population, generation_number)
    generation_number += 1

