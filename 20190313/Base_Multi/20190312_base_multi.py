from population import Population
from genetic_algorithm import GeneticAlgorithm
import time
import datetime
import os
import csv

POPULATION_SIZE = 10
GENERATION_SIZE = 10

def _print_population(pop, gen_number, file_name):
    print("-----------------------------------------------------------------------------")
    print("generation #", gen_number, " - ", pop.get_chromosomes()[0].get_genes(), " | Fittest chromosome fitness:", pop.get_chromosomes()[0].get_fitness())
    print("-----------------------------------------------------------------------------")

    num_of_stocks = len(pop.get_chromosomes()[0].get_genes())
    tickers = pop.get_chromosomes()[0].get_tickers()

    if os.path.exists('./result/' + file_name):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not
    writer = csv.writer(open('./result/' + file_name, append_write, newline=''))

    ticker_rows = []
    ticker_title = "Tradable Stock # " + str(num_of_stocks)
    ticker_rows.append(ticker_title)
    for num in range(num_of_stocks):
        ticker_rows.append(tickers[num])
    writer.writerows([ticker_rows])

    header_rows = []
    header_title = "Generation # " + str(gen_number)
    header_fitness_title = "| Fittest Chromosome Fitness"
    header_fitness = pop.get_chromosomes()[0].get_fitness()
    header_rows.append(header_title)
    for num in range(num_of_stocks):
        header_rows.append(pop.get_chromosomes()[0].get_genes()[num])
    header_rows.append(header_fitness_title)
    header_rows.append(header_fitness)
    writer.writerows([header_rows])

    index = 0
    for chromosome in pop.get_chromosomes():
        chromo_rows = []
        chromo_title = "chromosome #" + str(index)
        chromo_fitness_title = "| Fitness"
        chromo_fitness = chromosome.get_fitness()
        chromo_rows.append(chromo_title)
        for num in range(num_of_stocks):
            chromo_rows.append(chromosome.get_genes()[num])
        chromo_rows.append(chromo_fitness_title)
        chromo_rows.append(chromo_fitness)
        index += 1
        writer.writerows([chromo_rows])

def main(file_name):
    print("Find " + file_name + " for the further details.")
    population = Population(POPULATION_SIZE)
    population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
    _print_population(population, 0, file_name)

    generation_number = 1
    while generation_number < GENERATION_SIZE:
        population = GeneticAlgorithm.evolve(population)
        population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
        _print_population(population, generation_number, file_name)
        generation_number += 1

if __name__ == '__main__':
    file_name = "Kospi_base_result-" + str(datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")) + ".csv"
    Start_time = time.time()
    main(file_name)
    End_time = time.time()
    print("Done in: ", End_time - Start_time)
