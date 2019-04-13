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


def _print_population(pop, gen_number, file_name):

    if os.path.exists('../Result/' + str(MONTH) + '/' + file_name):
        append_write = 'a'  # append if already exists
    else:
        if not os.path.exists('../Result/' + str(MONTH) + '/'):
            os.makedirs('../Result/' + str(MONTH) + '/')
        append_write = 'w'  # make a new file if not
    writer = csv.writer(open('../Result/' + str(MONTH) + '/' + file_name, append_write, newline=''))

    best_chromosome = pop.get_chromosomes()[0]
    tickers = best_chromosome.get_tickers()
    num_of_stocks = len(tickers)
    ticker_rows = []
    ticker_title = "Tradable Stock # " + str(num_of_stocks)
    ticker_rows.append(ticker_title)
    for num in range(num_of_stocks):
        ticker_rows.append(tickers[num])
    writer.writerows([ticker_rows])

    header_rows = []
    header_title = "Generation #" + str(gen_number)
    header_fitness_title = " | Fittest chromosome fitness: "
    header_fitness = best_chromosome.get_fitness()
    header_rows.append(header_title)
    for num in range(num_of_stocks):
        header_rows.append(best_chromosome.get_genes()[num])
    header_rows.append(header_fitness_title)
    header_rows.append(header_fitness)
    writer.writerows([header_rows])

    # for count in range(650):
    #     logging.info("=", end="")
    #     logging.info("")
    # logging.info(header_title, " - ", header_fitness_title, header_fitness)

    index = 0
    for chromosome in pop.get_chromosomes():
        chromosome_row = []
        chromosome_title = "Chromosome #" + str(index)
        chromosome_fitness_title = "| Fitness: "
        pool = ThreadPool(processes=8)
        async_result = pool.apply_async(chromosome.get_fitness)
        chromosome_row.append(chromosome_title)
        for num in range(num_of_stocks):
            chromosome_row.append(chromosome.get_genes()[num])
            chromosome_row.append(chromosome_fitness_title)
        pool.close()
        chromosome_row.append(async_result.get())
        chromosome_roi_title = "| ROI: "
        chromosome_row.append(chromosome_roi_title)
        chromosome_row.append(chromosome.get_roi())
        index += 1
        writer.writerows([chromosome_row])


def main(file_name):
    day_list = scraper.days(KOSPI_TICKER, START_DATE, END_DATE)
    stock_price_list = scraper.stock_prices(day_list, KOSPI_TICKER, START_DATE, END_DATE)

    print("Find " + file_name + " for the further details.")
    population = Population(POPULATION_SIZE, day_list, stock_price_list)
    population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
    _print_population(population, 0, file_name)
    generation_number = 1
    while generation_number <= GENERATION_SIZE+1:
        population = GeneticAlgorithm.evolve(population, day_list, stock_price_list, POPULATION_SIZE)
        population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
        _print_population(population, generation_number, file_name)
        generation_number += 1

    print("BEST PF RESULT AFTER GA", population.get_chromosomes()[0])
    print("Number of stocks selected in the portfolio: ", population.get_chromosomes()[0].get_num_of_selected_stocks(), " | ROI: ", population.get_chromosomes()[0].get_roi(), " | RISK: ", population.get_chromosomes()[0].get_risk())
    print("Fittest chromosome fitness:", population.get_chromosomes()[0].get_fitness())
    for count in range(650):
        print("=", end="")
    print()


if __name__ == '__main__':
    START_DATE = 0
    END_DATE = 0

    MONTH = 12
    DAY_START = 1
    DAY_END = 31

    for MONTH_COUNT in range(MONTH):
        print("Month: ", MONTH_COUNT+1)
        START_DATE = datetime.datetime(2017, MONTH_COUNT+1, DAY_START)
        END_DATE = datetime.datetime(2017, MONTH_COUNT+1, DAY_END)
        TEST_NUM = 10
        # kospi200_scrap.kospi_data(START_DATE, END_DATE)
        # kospi200_scrap.fix_data(START_DATE, END_DATE)
        for i in range(TEST_NUM):
            file_name = "Kospi_200_portfolio_optimization-" + str(datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")) + ".csv"
            initiated = time.time()
            main(file_name)
            completed = time.time()
            print(i+1, "th Portfolio Optimization Using GA Completed In: ", initiated - completed, "Seconds.")
