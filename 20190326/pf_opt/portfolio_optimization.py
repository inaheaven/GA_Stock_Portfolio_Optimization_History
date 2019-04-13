from settings import *
from kospi_tickers import *
from population import Population
from genetic_algorithm import GeneticAlgorithm

import scraper
import save
import test_fund

import time
import datetime
from dateutil import relativedelta
from calendar import monthrange
import threading



def main(training_file_name, year, month, ga_start_date, ga_end_date, test_start_date, test_end_date):
    day_list = scraper.days(KOSPI_TICKER, ga_start_date, ga_end_date)
    stock_price_list = scraper.stock_prices(day_list, KOSPI_TICKER, ga_start_date, ga_end_date)
    test_day_list = scraper.days(KOSPI_TICKER, test_start_date, test_end_date)
    test_stock_price_list = scraper.stock_prices(test_day_list, KOSPI_TICKER, test_start_date, test_end_date)

    population = Population(POPULATION_SIZE, day_list, stock_price_list)
    population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
    save.save_population(population, 0, training_file_name, year, month)
    generation_number = 1

    while generation_number < GENERATION_SIZE:
        population = GeneticAlgorithm.evolve(population, day_list, stock_price_list, POPULATION_SIZE)
        population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
        save.save_population(population, generation_number, training_file_name, year, month)
        generation_number += 1

    best_chromosome = population.get_chromosomes()[0]
    save.print_best_population(best_chromosome, year, month, training_file_name)
    if generation_number == GENERATION_SIZE:
        monthly_best_file_name = "Kospi_200_portfolio_optimization-Monthly Best.csv"
        save.save_vars(year, month, monthly_best_file_name)
        save.save_best_generation(best_chromosome, year, month, monthly_best_file_name)
        test_fund.test_best_population(KOSPI_TICKER, best_chromosome, test_day_list, test_stock_price_list, year, month, monthly_best_file_name)

def main_threads(year, month, ga_start_date, ga_end_date, test_start_date, test_end_date):
    for i in range(TEST_NUM):
        training_file_name = "Kospi_200_portfolio_optimization-" + str(datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")) + ".csv"
        initiated = time.time()
        main(training_file_name, year, month, ga_start_date, ga_end_date, test_start_date, test_end_date)
        completed = time.time()
        print(i + 1, "th PORTFOLIO OPTIMIZATION FOR ", month, ",", year, "USING GA COMPLETED IN: ", completed - initiated, "SECONDS.")
        for count in range(650):
            print("=", end="")
        print()


if __name__ == '__main__':
    # SCRAP_START_DATE = datetime.datetime(YEAR, 1, 1)
    # SCRAP_END_DATE = datetime.datetime(2019, 12, 31)
    # kospi200_scrap.kospi_data(SCRAP_START_DATE, SCRAP_END_DATE)
    # kospi200_scrap.fix_data(SCRAP_START_DATE, END_DATE)
    threads = []
    YEAR_COUNT = YEAR
    # while YEAR_COUNT < 2019:
    for MONTH in range(MONTHS):
        MONTH_COUNT = MONTH + 1
        DAY_START = 1
        DAY_END = monthrange(YEAR_COUNT, MONTH_COUNT)[1]
        GA_START_DATE = datetime.datetime(YEAR_COUNT, MONTH_COUNT, DAY_START)
        GA_END_DATE = datetime.datetime(YEAR_COUNT, MONTH_COUNT, DAY_END)
        TEST_START_DATE = GA_START_DATE + relativedelta.relativedelta(months=1)
        TEST_END_DATE = GA_END_DATE + relativedelta.relativedelta(months=1)
        process = threading.Thread(target=main_threads, args=(YEAR_COUNT, MONTH_COUNT, GA_START_DATE, GA_END_DATE, TEST_START_DATE, TEST_END_DATE))
        process.start()
        threads.append(process)

    for process in threads:
        process.join()

        # YEAR_COUNT += 1
