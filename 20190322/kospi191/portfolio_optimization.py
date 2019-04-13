from population import Population
from genetic_algorithm import GeneticAlgorithm

import scraper
import kospi200_scrap

import glob
import time
import datetime
from calendar import monthrange
import os
import csv
from multiprocessing.pool import ThreadPool
import threading

TEST_NUM = 10
POPULATION_SIZE = 100
GENERATION_SIZE = 200
THREAD_LENGTH = 15
KOSPI_TICKER = []
file_names = [os.path.basename(x) for x in glob.glob('./kospi200/*.csv')]
for file_name in file_names:
    KOSPI_TICKER.append(os.path.splitext(file_name)[0])

# Dates Setting
YEAR = 2014
MONTHS = 12


def _print_population(pop, gen_number, training_file_name, year, month):
    if os.path.exists('../Result/' + str(year) + "/" + str(month) + '/' + training_file_name):
        append_write = 'a'  # append if already exists
    else:
        if not os.path.exists('../Result/' + str(year) + "/" + str(month) + '/'):
            os.makedirs('../Result/' + str(year) + "/" + str(month) + '/')
        append_write = 'w'  # make a new file if not
    writer = csv.writer(open('../Result/' + str(year) + "/" + str(month) + '/' + training_file_name, append_write, newline=''))

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


def main(training_file_name, year, month, start_date, end_date):
    day_list = scraper.days(KOSPI_TICKER, start_date, end_date)
    stock_price_list = scraper.stock_prices(day_list, KOSPI_TICKER, start_date, end_date)

    population = Population(POPULATION_SIZE, day_list, stock_price_list)
    population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
    _print_population(population, 0, training_file_name, year, month)
    generation_number = 1

    while generation_number <= GENERATION_SIZE:
        population = GeneticAlgorithm.evolve(population, day_list, stock_price_list, POPULATION_SIZE)
        population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
        _print_population(population, generation_number, training_file_name, year, month)
        generation_number += 1

    best_chromosome = population.get_chromosomes()[0]
    print("GA OPTIMIZATION ON KOSPI200 FINANCIAL DATA ON", month, ",", year, '-', training_file_name)
    print("BEST PF RESULT AFTER GA", best_chromosome)
    print("Number of stocks selected in the portfolio: ", best_chromosome.get_num_of_selected_stocks())
    print("ROI: ", best_chromosome.get_roi(), " | RISK: ", best_chromosome.get_risk())
    print("Fittest chromosome fitness:", best_chromosome.get_fitness())

    if generation_number == GENERATION_SIZE:
        monthly_best = []
        monthly_best_file_name = "Monthly Best-" + str(month) + "_" + str(year) + ".csv"
        monthly_best.append([year, month, best_chromosome, best_chromosome.get_fitness(), best_chromosome.get_roi()])
        if os.path.exists('../Result/' + str(year) + '/' + monthly_best_file_name):
            append_write = 'a'  # append if already exists
        else:
            append_write = 'w'  # make a new file if not
        writer2 = csv.writer(open('../Result/' + str(year) + '/' + monthly_best_file_name, append_write, newline=''))
        writer2.writerows([monthly_best])


def main_threads(year, month, start_date, end_date):
    for i in range(TEST_NUM):
        training_file_name = "Kospi_200_portfolio_optimization-" + str(datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")) + ".csv"
        initiated = time.time()
        main(training_file_name, year, month, start_date, end_date)
        completed = time.time()
        print(i + 1, "th PORTFOLIO OPTIMIZATION FOR ", year, "USING GA COMPLETED IN: ", completed - initiated, "SECONDS.")
        for count in range(650):
            print("=", end="")
        print()


if __name__ == '__main__':
    SCRAP_START_DATE = datetime.datetime(YEAR, 1, 1)
    SCRAP_END_DATE = datetime.datetime(2019, 12, 31)
    kospi200_scrap.kospi_data(SCRAP_START_DATE, SCRAP_END_DATE)
    # kospi200_scrap.fix_data(SCRAP_START_DATE, END_DATE)

    threads = []
    YEAR_COUNT = YEAR
    while YEAR_COUNT < 2019:
        for MONTH in range(MONTHS):
            MONTH_COUNT = MONTH + 1
            DAY_START = 1
            DAY_END = monthrange(YEAR_COUNT, MONTH_COUNT)[1]
            GA_START_DATE = datetime.datetime(YEAR_COUNT, MONTH_COUNT, DAY_START)
            GA_END_DATE = datetime.datetime(YEAR_COUNT, MONTH_COUNT, DAY_END)
            process = threading.Thread(target=main_threads, args=(YEAR_COUNT, MONTH_COUNT, GA_START_DATE, GA_END_DATE))
            process.start()
            threads.append(process)

        for process in threads:
            process.join()

        YEAR_COUNT += 1
