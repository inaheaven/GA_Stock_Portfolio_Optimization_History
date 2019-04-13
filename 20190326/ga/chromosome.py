from settings import *
from kospi_tickers import *

import fund_standardization

import random


class Chromosome:
    # a candidate solution
    def __init__(self, days, stock_prices):
        self._genes = []
        for i in range(len(KOSPI_TICKER)):
            if random.random() <= INITIAL_STOCK_SELCTION_RATE:
                self._genes.append(1)
            else:
                self._genes.append(0)
        self._days = days
        self._stock_prices = stock_prices
        self._initial_funds = INITIAL_FUNDS
        self._fee_rate = FEE_RATE
        self._tax_rate = TAX_RATE
        self._risk_free_rate = RISK_FREE_RATE
        self._ticker = KOSPI_TICKER

        self._num_of_stocks = len(KOSPI_TICKER)
        self._num_of_selected_stocks = fund_standardization.num_of_selected_stocks(self._genes, self._num_of_stocks)
        self._allocated_fund_amount = 0
        if self._num_of_selected_stocks != 0:
            self._allocated_fund_amount = self._initial_funds // self._num_of_selected_stocks
            self._remainder_of_pf = 0
        else:
            self._allocated_fund_amount = 0
            self._remainder_of_pf = self._initial_funds

        self._allocated_fund = fund_standardization.allocated_funds(self._genes, self._allocated_fund_amount, self._num_of_stocks)
        # print("_allocated_fund", _allocated_fund)
        self._remainder_of_pf = fund_standardization.remainder_of_pfs(self._initial_funds, self._allocated_fund_amount, self._num_of_selected_stocks)
        # print("self._days", self._days)
        # print("_stock_price", _stock_price)
        self._share = fund_standardization.shares(self._genes, self._num_of_stocks, self._allocated_fund, self._stock_prices, FEE_RATE)
        # print("_share", _share)
        self._handling_fee = fund_standardization.handling_fees(self._genes, self._days, self._num_of_stocks, self._share, self._stock_prices, FEE_RATE)
        # print("_handling_fee", _handling_fee)
        self._remainder_of_stock = fund_standardization.remainder_of_stocks(self._genes, self._num_of_stocks, self._allocated_fund, self._stock_prices, self._share, self._handling_fee)
        # print("_remainder_of_stock", _remainder_of_stock)
        self._return = fund_standardization.returns(self._genes, self._days, self._num_of_stocks, self._share, self._stock_prices)
        # print("_return", _return)
        self._securities_transaction_tax = fund_standardization.securities_transaction_taxes(self._genes, self._days, self._num_of_stocks, self._share, self._stock_prices, TAX_RATE)
        # print("_securities_transaction_tax", _securities_transaction_tax)
        self._funds_standardization = fund_standardization.funds_standardizations(self._genes, self._num_of_stocks, self._days, self._allocated_fund, self._handling_fee, self._return, self._securities_transaction_tax, self._remainder_of_stock)
        # print("_funds_standardization", _funds_standardization)
        self._pf_funds_standardization = fund_standardization.pf_funds_standardizations(self._days, self._num_of_stocks, self._funds_standardization, self._remainder_of_pf)
        # print("_pf_funds_standardization", _pf_funds_standardization)
        self._roi = fund_standardization.rois(self._pf_funds_standardization, self._initial_funds)
        # print("_roi", _roi)
        self._risk = fund_standardization.risks(self._days, self._pf_funds_standardization)
        # print("_risk", _risk)
        self._fitness = fund_standardization.fitnesses(self._roi, self._risk, RISK_FREE_RATE)
        # print("Fitness: ", self._fitness)

    def get_tickers(self):
        return self._ticker

    def get_genes(self):
        return self._genes

    def get_fitness(self):
        return self._fitness

    def get_num_of_stocks(self):
        return self._num_of_stocks

    def get_num_of_selected_stocks(self):
        return self._num_of_selected_stocks

    def get_rois(self):
        return self._roi

    def get_risks(self):
        return self._risk

    def __str__(self):
        return self._genes.__str__()