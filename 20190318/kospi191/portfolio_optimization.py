from population import Population
from genetic_algorithm import GeneticAlgorithm

import scraper

import glob
import time
import datetime
import os
import csv
from multiprocessing.pool import ThreadPool

POPULATION_SIZE = 100
GENERATION_SIZE = 200
KOSPI_TICKER = []
file_names = [os.path.basename(x) for x in glob.glob('./kospi200/*.csv')]
for file_name in file_names:
    KOSPI_TICKER.append(os.path.splitext(file_name)[0])


STARTDATE = datetime.datetime(2017, 7, 1)
ENDDATE = datetime.datetime(2017, 7, 31)


def _print_population(pop, gen_number, file_name):
    best_fit = pop.get_chromosomes()[0].get_fitness()
    for count in range(650):
        print("=", end="")
    print()
    print("Generation #", gen_number, " - ", pop.get_chromosomes()[0].get_genes(), " | Fittest chromosome fitness:", best_fit)


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
    for chromosome in pop.get_chromosomes():
        chromo_row = []
        chromo_title = "chromosome #" + str(index)
        chromo_fitness_title = "| Fitness: "
        pool = ThreadPool(processes=8)
        async_result = pool.apply_async(chromosome.get_fitness)
        chromo_row.append(chromo_title)
        for num in range(num_of_stocks):
            chromo_row.append(chromosome.get_genes()[num])
        chromo_row.append(chromo_fitness_title)
        pool.close()
        chromo_fitness_title = "| ROI: "
        chromo_row.append(chromo_fitness_title)
        chromo_row.append(chromosome.get_roi())
        chromo_row.append(async_result.get())
        index += 1
        writer.writerows([chromo_row])

def main(file_name):

    days = scraper.days(KOSPI_TICKER, STARTDATE, ENDDATE)
    stock_prices = scraper.stock_prices(days, KOSPI_TICKER, STARTDATE, ENDDATE)

    print("Find " + file_name + " for the further details.")
    population = Population(POPULATION_SIZE, days, stock_prices)
    population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
    _print_population(population, 1, file_name)
    generation_number = 2
    while generation_number <= GENERATION_SIZE+1:
        gen_start_time = time.time()

        population = GeneticAlgorithm.evolve(population, days, stock_prices)
        population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
        _print_population(population, generation_number, file_name)
        generation_number += 1

        gen_end_time = time.time()
        print("generation created in ", gen_end_time - gen_start_time, "Seconds.")

    for count in range(650):
        print("=", end="")
    print()
    print("BEST PF RESULT AFTER GA", population.get_chromosomes()[0])
    print("Num of stocks: ", population.get_chromosomes()[0].get_num_of_selected_stocks(), " | ROI: ", population.get_chromosomes()[0].get_roi(), " | RISK: ", population.get_chromosomes()[0].get_risk())
if __name__ == '__main__':

    for i in range(10):
        # kospi200_scrap.kospi_data(STARTDATE, ENDDATE)
        # kospi200_scrap.fix_data(STARTDATE, ENDDATE)

        file_name = "kospi_200_portfolio_optimization-" + str(datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")) + ".csv"
        Start_time = time.time()
        main(file_name)
        End_time = time.time()
        print(i, "th Porfolio Optimization Using GA Done In: ", End_time - Start_time, "Seconds.")
