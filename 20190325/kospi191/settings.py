import glob
import os

STOCK_SELCTION_RATE = 0.2
NUM_OF_ELITE_CHROMOSOMES = 10
TOURNAMENT_SELECTION_SIZE = 80
MUTATION_RATE = 0.15
FEE_RATE = 0.000015
TAX_RATE = 0.003
RISK_FREE_RATE = 0.02
INITIAL_FUNDS = 100000000
INITIAL_STOCK_SELCTION_RATE = 0.1
TEST_NUM = 3
POPULATION_SIZE = 100
GENERATION_SIZE = 200
KOSPI_TICKER = []
file_names = [os.path.basename(x) for x in glob.glob('./kospi200/*.csv')]
for file_name in file_names:
    KOSPI_TICKER.append(os.path.splitext(file_name)[0])
NUM_OF_STOCKS = len(KOSPI_TICKER)

# Dates Setting
YEAR = 2018
MONTHS = 12
