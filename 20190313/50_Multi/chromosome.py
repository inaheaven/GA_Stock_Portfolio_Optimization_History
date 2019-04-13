import os
import glob
import datetime
import random

import fund_standardization

PORTAL = 'yahoo'
file_names = [os.path.basename(x) for x in glob.glob('./kospi200/*.csv')]
KOSPI_TICKER = []
count = 0
for file_name in file_names:
    KOSPI_TICKER.append(os.path.splitext(file_name)[0])
    count += 1
    if count >= 50:
        break
# KOSPI_TICKER = ['000070.KS', '000080.KS', '000100.KS', '000120.KS', '000150.KS', '000210.KS', '000240.KS', '000270.KS', '000640.KS', '000660.KS']
# KOSPI_TICKER = ['000070.KS', '000080.KS', '000100.KS', '000120.KS', '000150.KS']
NUM_OF_STOCKS = len(KOSPI_TICKER)

STARTDATE = datetime.datetime(2018, 1, 1)
ENDDATE = datetime.datetime(2018, 1, 31)

FEE_RATE = 0.000015
TAX_RATE = 0.003
RISK_FREE_RATE = 0.02
INITIAL_FUNDS = 100000000
STOCK_SELCTION_RATE = 0.1

class Chromosome:
    # represents a candidate solution
    def __init__(self):
        self._genes = []
        for i in range(NUM_OF_STOCKS):
            if random.random() <= STOCK_SELCTION_RATE:
                self._genes.append(1)
            else:
                self._genes.append(0)
        self._ticker = KOSPI_TICKER

    def get_tickers(self):
        return self._ticker

    def get_genes(self):
        return self._genes

    def get_fitness(self):
        _num_of_selected_stocks = fund_standardization.num_of_selected_stocks(self._genes, NUM_OF_STOCKS)
        _allocated_fund_amount = 0
        if _num_of_selected_stocks != 0:
            _allocated_fund_amount = INITIAL_FUNDS // _num_of_selected_stocks
        else:
            # print("NO STOCK HAS BEEN SELECTED")
            _fitness = 0.0
            _allocated_fund_amount = 0
            _remainder_of_pf = INITIAL_FUNDS

        _allocated_fund = fund_standardization.allocated_funds(self._genes, _allocated_fund_amount, NUM_OF_STOCKS)
        print("_allocated_fund", _allocated_fund)
        _remainder_of_pf = fund_standardization.remainder_of_pfs(INITIAL_FUNDS, _allocated_fund_amount, _num_of_selected_stocks)
        print("_remainder_of_pf", _remainder_of_pf)
        _day = fund_standardization.days(KOSPI_TICKER, STARTDATE, ENDDATE)
        print("_day", _day)
        _stock_price = fund_standardization.stock_prices(self._genes, _day, KOSPI_TICKER, STARTDATE, ENDDATE)
        print("_stock_price", _stock_price)
        _share = fund_standardization.shares(self._genes, NUM_OF_STOCKS, _allocated_fund, _stock_price, FEE_RATE)
        print("_share", _share)
        _handling_fee = fund_standardization.handling_fees(self._genes, _day, NUM_OF_STOCKS, _share, _stock_price, FEE_RATE)
        print("_handling_fee", _handling_fee)
        _remainder_of_stock = fund_standardization.remainder_of_stocks(self._genes, NUM_OF_STOCKS, _allocated_fund, _stock_price, _share, _handling_fee)
        print("_remainder_of_stock", _remainder_of_stock)
        _return = fund_standardization.returns(self._genes, _day, NUM_OF_STOCKS, _share, _stock_price)
        print("_return", _return)
        _securities_transaction_tax = fund_standardization.securities_transaction_taxes(self._genes, _day, NUM_OF_STOCKS, _share, _stock_price, TAX_RATE)
        print("_securities_transaction_tax", _securities_transaction_tax)
        _funds_standardization = fund_standardization.funds_standardizations(self._genes, KOSPI_TICKER, NUM_OF_STOCKS, _day, _allocated_fund, _handling_fee, _return, _securities_transaction_tax, _remainder_of_stock)
        print("_funds_standardization", _funds_standardization)
        _pf_funds_standardization = fund_standardization.pf_funds_standardizations(self._genes, _day, NUM_OF_STOCKS, _funds_standardization, _remainder_of_pf)
        print("_pf_funds_standardization", _pf_funds_standardization)
        _roi = fund_standardization.rois(_pf_funds_standardization, INITIAL_FUNDS, _day)
        print("_roi", _roi)
        _risk = fund_standardization.risks(_day, _pf_funds_standardization)
        print("_risk", _risk)
        _fitness = fund_standardization.fitnesses(_roi, _risk, RISK_FREE_RATE)
        print("_fitness: ", _fitness)
        return _fitness

    def __str__(self):
        return self._genes.__str__()