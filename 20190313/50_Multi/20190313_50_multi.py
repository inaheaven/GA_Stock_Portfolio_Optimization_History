from population import Population
from genetic_algorithm import GeneticAlgorithm

import time
import datetime
import os
import csv
from multiprocessing.pool import ThreadPool

POPULATION_SIZE = 100
GENERATION_SIZE = 50


def _print_population(pop, gen_number, file_name):
    best_fit = pop.get_chromosomes()[0].get_fitness()
    print("-----------------------------------------------------------------------------")
    print("generation #", gen_number, " - ", pop.get_chromosomes()[0].get_genes(), " | Fittest chromosome fitness:", best_fit)
    print("-----------------------------------------------------------------------------")

    tickers = pop.get_chromosomes()[0].get_tickers()
    num_of_stocks = len(tickers)

    if os.path.exists('../Result/' + file_name):
        append_write = 'a'  # append if already exists
    else:
        append_write = 'w'  # make a new file if not
    writer = csv.writer(open('../Result/' + file_name, append_write, newline=''))

    ticker_rows = []
    ticker_title = "Tradable Stock # " + str(num_of_stocks)
    ticker_rows.append(ticker_title)
    for num in range(num_of_stocks):
        ticker_rows.append(tickers[num])
    writer.writerows([ticker_rows])

    header_rows = []
    header_title = "Generation # " + str(gen_number)
    header_fitness_title = "| Fittest Chromosome Fitness"
    header_fitness = best_fit
    header_rows.append(header_title)
    for num in range(num_of_stocks):
        header_rows.append(pop.get_chromosomes()[0].get_genes()[num])
    header_rows.append(header_fitness_title)
    header_rows.append(header_fitness)
    writer.writerows([header_rows])

    index = 0
    chromo_rows = []
    for chromosome in pop.get_chromosomes():
        chromo_row = []
        chromo_title = "chromosome #" + str(index)
        chromo_fitness_title = "| Fitness"
        # chromo_fitness = chromosome.get_fitness()
        pool = ThreadPool(processes=8)
        async_result = pool.apply_async(chromosome.get_fitness)
        chromo_row.append(chromo_title)
        for num in range(num_of_stocks):
            chromo_row.append(chromosome.get_genes()[num])
        chromo_row.append(chromo_fitness_title)
        chromo_row.append(async_result.get())
        chromo_rows.append(chromo_row)
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
    file_name = "Kospi_50_result-" + str(datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")) + ".csv"
    Start_time = time.time()
    main(file_name)
    End_time = time.time()
    print("Done in: ", End_time - Start_time)
