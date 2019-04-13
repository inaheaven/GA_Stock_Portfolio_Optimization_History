import datetime
import fund_standardization
import random


INITIAL_FUNDS = 100000000
NUM_OF_STOCKS = 10
NUM_OF_CHROMOSOME = 10
FEE_RATE = 0.000015
TAX_RATE = 0.003
RISK_FREE_RATE = 0.02
KOSPI_TICKER = ['000070.KS', '000080.KS', '000100.KS', '000120.KS', '000150.KS', '000210.KS', '000240.KS', '000270.KS', '000640.KS', '000660.KS']
# KOSPI_TICKER = ['000070.KS', '000080.KS', '000100.KS']
PORTAL = 'yahoo'
STARTDATE = datetime.datetime(2018, 1, 1)
ENDDATE = datetime.datetime(2018, 12, 31)

# NUM_OF_ELITE_CHROMOSOMES = 1
# TOURNAMENT_SELECTION_SIZE = 4
# MUTATION_RATE = 0.25


class Chromosome:
    # represents a candidate solution
    def __init__(self):
        self._name = KOSPI_TICKER
        self._num_of_selected_stocks = 0
        self._genes = []

        for i in range(NUM_OF_STOCKS):
            if random.random() >= 0.5:
                self._genes.append(1)
                self._num_of_selected_stocks +=1
            else:
                self._genes.append(0)
        print("genes: ", self._genes)
        print("num of selected stocks: ", self._num_of_selected_stocks)
        if self._num_of_selected_stocks != 0:
            self._allocated_fund_amount = INITIAL_FUNDS // self._num_of_selected_stocks
        else:
            print("not buying any stocks")
            return
        print("allocated_fund_amount: ", self._allocated_fund_amount)
        self._allocated_fund = fund_standardization.allocated_funds(self._genes, self._allocated_fund_amount, NUM_OF_STOCKS)
        print("allocated fund: ", self._allocated_fund)
        self._remainder_of_pf = fund_standardization.remainder_of_pfs(INITIAL_FUNDS, self._allocated_fund_amount, self._num_of_selected_stocks)
        print("remainder_of_pf: ", self._remainder_of_pf)
        self._day = fund_standardization.days(KOSPI_TICKER, STARTDATE, ENDDATE)
        print("days of trading: ", self._day)
        self._stock_price = fund_standardization.stock_prices(self._genes, KOSPI_TICKER, STARTDATE, ENDDATE)
        print("stock_price: ", self._stock_price)
        self._share = fund_standardization.shares(self._genes, NUM_OF_STOCKS, self._allocated_fund, self._stock_price, FEE_RATE)
        print("share: ", self._share)
        self._handling_fee = fund_standardization.fees(self._genes, NUM_OF_STOCKS, self._share, self._stock_price, FEE_RATE)
        print("handling fee: ", self._handling_fee)
        self._remainder_of_stock = fund_standardization.remainder_of_stocks(self._genes, NUM_OF_STOCKS, self._allocated_fund, self._stock_price, self._share, self._handling_fee)
        print("remainder of stock: ", self._remainder_of_stock)
        self._return = fund_standardization.returns(self._genes, NUM_OF_STOCKS, self._share, self._stock_price)
        print("return: ", self._return)
        self._securities_transaction_tax = fund_standardization.securities_transaction_taxes(self._genes, NUM_OF_STOCKS, self._share, self._stock_price, TAX_RATE)
        print("transaction tax: ", self._securities_transaction_tax)
        self._first_funds_standardization = fund_standardization.funds_standardizations(self._genes, NUM_OF_STOCKS, 1, self._allocated_fund, self._handling_fee, self._return, self._securities_transaction_tax, self._remainder_of_stock)
        print("first funds standardization: ", self._first_funds_standardization)
        self._funds_standardization = fund_standardization.funds_standardizations(self._genes, NUM_OF_STOCKS, self._day, self._allocated_fund, self._handling_fee, self._return, self._securities_transaction_tax, self._remainder_of_stock)
        print("funds standardization: ", self._funds_standardization)
        self._first_pf_funds_standardization = fund_standardization.pf_funds_standardizations(self._genes, self._first_funds_standardization, self._remainder_of_pf)
        print("first pf_funds standardization: ", self._first_pf_funds_standardization)
        self._pf_funds_standardization = fund_standardization.pf_funds_standardizations(self._genes, self._funds_standardization, self._remainder_of_pf)
        print("pf_funds standardization: ", self._pf_funds_standardization)

        print("\n\n=====================================================")
        self._roi = fund_standardization.rois(self._pf_funds_standardization, INITIAL_FUNDS)
        print("roi: ", self._roi)
        self._risk = fund_standardization.risks(self._first_pf_funds_standardization, self._pf_funds_standardization)
        print("risk: ", self._risk)
        self._fitness = fund_standardization.fitnesses(self._roi, self._risk, RISK_FREE_RATE)
        print("fitness/ Sharpe Ratio: ", self._fitness)
        print("return: ", (self._pf_funds_standardization - INITIAL_FUNDS)/INITIAL_FUNDS)
    def get_genes(self):
        return self._genes

    def get_allocated_fund(self):
        return self._allocated_fund

    def get_remainder_of_pf(self):
        return self._allocated_fund

    def get_stock_price(self):
        return self._stock_price

    def get_share(self):
        return self._share

    def get_handling_fee(self):
        return self._handling_fee

    def get_remainder_of_stock(self):
        return self._remainder_of_stock

    def get_return(self):
        return self._return

    def get_securities_transaction_tax(self):
        return self._securities_transaction_tax

    def get_funds_standardization(self):
        return self._funds_standardization

    def get_pf_funds_standardization(self):
        return self._pf_funds_standardization

    def get_roi(self):
        return self._roi

    def get_fitness(self):

        return self._fitness

    # def get_roi(self):
    #     return self.final_funds -
    def __str__(self):
        return self._genes.__str__()

class Population:
    # population of candidate solutions
    def __init__(self, size):
        self._chromosomes = []
        i = 0
        while i < size:
            self._chromosomes.append(Chromosome())
            i += 1

    def get_chromosomes(self):
        return self._chromosomes



# class GeneticAlgorithm:
#     # selection, crossover, mutation and elitism logic
#     @staticmethod
#     def evolve(pop):
#         return GeneticAlgorithm._mutate_population(GeneticAlgorithm._crossover_population(pop))
#
#     @staticmethod
#     def _mutate_population(pop):
#         for i in range(NUM_OF_ELITE_CHROMOSOMES, POPULATION_SIZE):
#             GeneticAlgorithm._mutate_chromosome(pop.get_chromosomes()[i])
#         return pop
#
#     @staticmethod
#     def _crossover_population(pop):
#         crossover_pop = Population(0)
#         for i in range(NUM_OF_ELITE_CHROMOSOMES):
#             crossover_pop.get_chromosomes().append(pop.get_chromosomes()[i])
#             while i < POPULATION_SIZE:
#                 chromosome1 = GeneticAlgorithm._select_tournament_population(pop).get_chromosomes()[0]
#                 chromosome2 = GeneticAlgorithm._select_tournament_population(pop).get_chromosomes()[0]
#                 crossover_pop.get_chromosomes().append(GeneticAlgorithm._crossover_chromosomes(chromosome1, chromosome2))
#                 i += 1
#         return crossover_pop
#
#     @staticmethod
#     def _crossover_chromosomes(chromosome1, chromosome2):
#         crossover_chrom = Chromosome()
#         for i in range(TARGET_CHROMOSOME.__len__()):
#             if random.random() >= 0.5:
#                 crossover_chrom.get_genes()[i] = chromosome1.get_genes()[i]
#             else:
#                 crossover_chrom.get_genes()[i] = chromosome2.get_genes()[i]
#         return crossover_chrom
#
#     @staticmethod
#     def _mutate_chromosome(chromosome):
#         for i in range(TARGET_CHROMOSOME.__len__()):
#            if random.random() < MUTATION_RATE:
#                if random.random() < 0.5:
#                    chromosome.get_genes()[i] = 1
#                else:
#                    chromosome.get_genes()[i] = 0
#     @staticmethod
#     def _select_tournament_population(pop):
#         tournament_pop = Population(0)
#         i = 0
#         while i< TOURNAMENT_SELECTION_SIZE:
#             tournament_pop.get_chromosomes().append(pop.get_chromosomes()[random.randrange(0, POPULATION_SIZE)])
#             i += 1
#         tournament_pop.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse=True)
#         return  tournament_pop
#
def _print_population(pop, gen_number):
    print("\n----------------------------------------------")
    print("generation #", gen_number, "| Fittest chromosome fitness:", pop.get_chromosomes()[0].get_fitness())
    print("----------------------------------------------")
    i = 0
    for x in pop.get_chromosomes():
        print("chromosome # ", i, ":", x, "| Fitness: ", x.get_fitness(), "| Allocated Funds: ", x.get_allocated_fund(), "| Prices: ", x.get_stock_price(), "| Shares: ", x.get_share(), "| Remainder: ", x.get_remainder_of_stock(), "| Funds Standardization: ", x.get_funds_standardization())
        i += 1


population = Population(1)
population.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse=True)
_print_population(population, 0)
generation_number = 1
# while population.get_chromosomes()[0].get_fitness() < TARGET_CHROMOSOME.__len__():
#     population = GeneticAlgorithm.evolve(population)
#     population.get_chromosomes().sort(key=lambda x: x.get_fitness(), reverse=True)
#     _print_population(population, generation_number)
#     generation_number += 1
#
