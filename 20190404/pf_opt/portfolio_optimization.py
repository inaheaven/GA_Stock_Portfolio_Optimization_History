from settings_rates import *
from settings_kospi import *

from population import Population
from genetic_algorithm import GeneticAlgorithm

import scraper
import save
import test_fund

import time
import datetime
from dateutil import relativedelta
import multiprocessing as mp


def main(year, month, ga_start_date, ga_end_date, test_start_date, test_end_date, index):
    initiated_time = time.time()
    training_file_name = "Kospi_200_portfolio_optimization-" + str(datetime.datetime.now().strftime("%Y%m%d_%H_%M_%S")) + ".csv"

    day_list = scraper.days(KOSPI_TICKER, ga_start_date, ga_end_date)
    stock_price_list = scraper.stock_prices(day_list, KOSPI_TICKER, ga_start_date, ga_end_date)
    test_day_list = scraper.days(KOSPI_TICKER, test_start_date, test_end_date)
    test_stock_price_list = scraper.stock_prices(test_day_list, KOSPI_TICKER, test_start_date, test_end_date)

    population = Population(POPULATION_SIZE, day_list, stock_price_list)
    population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
    save.save_population(population, 0, year, month, training_file_name)
    generation_number = 1
    while generation_number < GENERATION_SIZE:
        population = GeneticAlgorithm.evolve(population, day_list, stock_price_list, POPULATION_SIZE)
        population.get_chromosomes().sort(key=lambda chromosome: chromosome.get_fitness(), reverse=True)
        save.save_population(population, generation_number, year, month, training_file_name)
        generation_number += 1

    if generation_number == GENERATION_SIZE:
        completed_time = time.time()
        print(index + 1, "th GA GENERATION OF PORTFOLIO OPTIMIZATION FOR ", test_start_date, ",", test_end_date,"COMPLETED IN", completed_time - initiated_time, "SECONDS.")
        best_chromosome = population.get_chromosomes()[0]
        test_fund.test_best_population(best_chromosome, test_day_list, test_stock_price_list, year, month, ga_start_date, ga_end_date, test_start_date, test_end_date)


def multiple_term(month, year, ga_start_date, ga_end_date, test_start_date, test_end_date):
    for index in range(TEST_NUM):
        main(year, month, ga_start_date, ga_end_date, test_start_date, test_end_date, index)


def multiple_quarter(year_index):
    weekly_threads = []
    for month_index in range(1, MONTHS, 1):
        day_start = 1
        ga_start_date = datetime.datetime(year_index, month_index, day_start)
        ga_end_date = ga_start_date + relativedelta.relativedelta(months=3)
        test_start_date = ga_end_date
        test_end_date = test_start_date + relativedelta.relativedelta(months=1)

        weekly_process = mp.Process(target=multiple_term, args=(month_index, year_index, ga_start_date, ga_end_date, test_start_date, test_end_date))
        weekly_process.start()
        weekly_threads.append(weekly_process)

    for weekly_process in weekly_threads:
        weekly_process.join()

# def multiple_month(year_index):
#     monthly_threads = []

#     for MONTH in range(1, MONTHS, 1):
#         day_start = 1
#         day_end = monthrange(year_index, MONTH+2)[1]
#         ga_start_date = datetime.datetime(year_index, MONTH, day_start)
#         ga_end_date = datetime.datetime(year_index, MONTH+2, day_end)
#         test_start_date = ga_start_date + relativedelta.relativedelta(months=3)
#         test_end_date = test_start_date + relativedelta.relativedelta(months=1)
#         print("ga_start_date", ga_start_date, "ga_end_date", ga_end_date)
#         print("test_start_date", test_start_date, "test_end_date", test_end_date)
#         monthly_process = mp.Process(target=multiple_term, args=(MONTH, year_index, ga_start_date, ga_end_date, test_start_date, test_end_date))
#         monthly_process.start()
#         monthly_threads.append(monthly_process)
#     for monthly_process in monthly_threads:
#
#         monthly_process.join()


if __name__ == '__main__':
    # SCRAP_START_DATE = datetime.datetime(YEAR, 1, 1)
    # SCRAP_END_DATE = datetime.datetime(2019, 12, 31)
    # kospi200_scrap.kospi_data(SCRAP_START_DATE, SCRAP_END_DATE)
    # kospi200_scrap.fix_data(SCRAP_START_DATE, END_DATE)
    total_initiated_time = time.time()
    save.save_vars()
    annual_threads = []
    for year in range(YEARS, 2018, 1):
        annual_process = mp.Process(target=multiple_quarter, args=(year,))
        annual_process.start()
        annual_threads.append(annual_process)

    for annual_process in annual_threads:
        annual_process.join()

    total_completed_time = time.time()
    print((total_completed_time-total_initiated_time)/60, "MINUTES HAVE BEEN SPENT")









