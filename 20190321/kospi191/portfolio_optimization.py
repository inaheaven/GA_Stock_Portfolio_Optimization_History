from population import Population
from genetic_algorithm import GeneticAlgorithm

import scraper

import glob
import time
import datetime
from calendar import monthrange
import os
import csv
from multiprocessing.pool import ThreadPool
import threading

# import logging

TEST_NUM = 10
POPULATION_SIZE = 100
GENERATION_SIZE = 200
THREAD_LENGTH = 15
KOSPI_TICKER = []
file_names = [os.path.basename(x) for x in glob.glob('./kospi200/*.csv')]
for file_name in file_names:
    KOSPI_TICKER.append(os.path.splitext(file_name)[0])

# Dates Setting
YEAR = 2017
MONTH = 12

def _print_population(pop, gen_number, file_name, month_count):

    if os.path.exists('../Result/' + str(month_count) + '/' + file_name):
        append_write = 'a'  # append if already exists
    else:
        if not os.path.exists('../Result/' + str(month_count) + '/'):
            os.makedirs('../Result/' + str(month_count) + '/')
        append_write = 'w'  # make a new file if not
    writer = csv.writer(open('../Result/' + str(month_count) + '/' + file_name, append_write, newline=''))

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
        chromosome_roi_title = "| ROI: "
        pool = ThreadPool(processes=THREAD_LENGTH)
        async_result = pool.apply_async(chromosome.get_fitness)
        chromosome_row.append(chromosome_title)
        for num in range(num_of_stocks):
            chromosome_row.append(chromosome.get_genes()[num])
        pool.close()
        chromosome_row.append(chromosome_fitness_title)
        chromosome_row.append(async_result.get())
        chromosome_row.append(chromosome_roi_title)
        chromosome_row.append(chromosome.get_roi())
        index += 1
        writer.writerows([chromosome_row])


def main(file_name, month, start_date, end_date):
    day_list = scraper.days(KOSPI_TICKER, start_date, end_date)
    stock_price_list = scraper.stock_prices(day_list, KOSPI_TICKER, start_date, end_date)

    # print(month_count, ": Find " + file_name + " for the further details.")
    population = Population(POPULATION_SIZE, day_list, stock_price_list)
    population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
    _print_population(population, 0, file_name, month)
    generation_number = 1
    while generation_number <= GENERATION_SIZE+1:
        population = GeneticAlgorithm.evolve(population, day_list, stock_price_list, POPULATION_SIZE)
        population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
        _print_population(population, generation_number, file_name, month)
        generation_number += 1
    print("GA OPTIMIZATION ON KOSPI200 FINANCIAL DATA ON", month, ",", YEAR)
    print("BEST PF RESULT AFTER GA", population.get_chromosomes()[0])
    print("Number of stocks selected in the portfolio: ", population.get_chromosomes()[0].get_num_of_selected_stocks(), " | ROI: ", population.get_chromosomes()[0].get_roi(), " | RISK: ", population.get_chromosomes()[0].get_risk())
    print("Fittest chromosome fitness:", population.get_chromosomes()[0].get_fitness())

def main_threads(month, start_date, end_date):
    # kospi200_scrap.kospi_data(START_DATE, END_DATE)
    # kospi200_scrap.fix_data(START_DATE, END_DATE)
    for i in range(TEST_NUM):
        file_name = "Kospi_200_portfolio_optimization-" + str(
            datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")) + ".csv"
        initiated = time.time()
        main(file_name, month, start_date, end_date)
        completed = time.time()
        print(i + 1, "th PORTFOLIO OPTIMIZATION USING GA COMPLETED IN: ", completed - initiated, "SECONDS.")
        for count in range(650):
            print("=", end="")
        print()


if __name__ == '__main__':
    threads = []
    for MONTH_COUNT in range(MONTH):
        MONTH_COUNT = MONTH_COUNT + 1
        DAY_START = 1
        DAY_END = monthrange(YEAR, MONTH_COUNT)[1]
        start_date = datetime.datetime(YEAR, MONTH_COUNT, DAY_START)
        end_date = datetime.datetime(YEAR, MONTH_COUNT, DAY_END)
        process = threading.Thread(target=main_threads, args=(MONTH_COUNT, start_date, end_date))
        process.start()
        threads.append(process)

    for process in threads:
        process.join()


