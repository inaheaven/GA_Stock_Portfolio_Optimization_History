import numpy as np
import pandas_datareader.data as web
import statistics

def allocated_funds(genes, allocated_fund_amount, num_of_stocks):
    allocated_fund = []
    for index in range(num_of_stocks):
        if genes[index] == 1:
            allocated_fund.append(allocated_fund_amount)
        else:
            allocated_fund.append(0)
    return allocated_fund

def remainder_of_pfs(initial_fund, allocated_fund, num_of_selected_stocks):
    remainder_of_pf = initial_fund - np.sum(allocated_fund) * num_of_selected_stocks
    return remainder_of_pf

def days(kospi_tickers, startdate, enddate):
    kospi_tickers_count = len(web.DataReader(kospi_tickers[0], "yahoo", startdate, enddate)['Adj Close'])
    return kospi_tickers_count

def stock_prices(genes, kospi_tickers, startdate, enddate):
    stock_price = []
    count = 0
    for ticker in kospi_tickers:
        kospi_tickers_count = len(web.DataReader(ticker, "yahoo", startdate, enddate)['Adj Close'])
        price = []
        # if genes[count] == 1:
        for index in range(kospi_tickers_count):
            price.append((float(web.DataReader(ticker, "yahoo", startdate, enddate)['Adj Close'][index])))
        stock_price.append(price)
        # else:
        #     for index in range(kospi_tickers_count):
        #         price.append(0)
        #     stock_price.append(price)
        count += 1
    # return stock_price
    return stock_price

def shares(genes, num_of_stocks, allocated_funds, stock_price, rate):
    share = []
    for index in range(num_of_stocks):
        if genes[index] == 1:
            share.append(allocated_funds[index] // (stock_price[index][0] + stock_price[index][0] * rate))
        else:
            share.append(0)
    # print("share", share)
    return share

def fees(genes, num_of_stocks, share, stock_price, rate):
    fee = []
    for index in range(num_of_stocks):
        if genes[index] == 1:
            fee.append(share[index] * stock_price[index][0] * rate)
        else:
            fee.append(0)
    # print("fee", fee)
    return  fee

def remainder_of_stocks(genes, num_of_stocks, allocated_funds, stock_price, share, handling_fee):
    remainder = []
    for index in range(num_of_stocks):
        if genes[index] == 1:
            remainder.append(np.floor(allocated_funds[index] - (stock_price[index][0] * share[index]) - handling_fee[1]))
        else:
            remainder.append(0)
    # print("remainder", remainder)
    return remainder

def returns(genes, num_of_stocks, share, stock_price):
    cash= []
    for index in range(num_of_stocks):
        kospi_tickers_count = len(stock_price[index])
        if genes[index] == 1:
            cash.append(stock_price[index][kospi_tickers_count-1] * share[index])
        else:
            cash.append(0)
    # print(cash)
    return cash

def securities_transaction_taxes(genes, num_of_stocks, share, stock_price, rate):
    tax = []
    for index in range(num_of_stocks):
        if genes[index] == 1:
            tax.append(share[index] * stock_price[index][0] * rate)
        else:
            tax.append(0)
    return tax

def funds_standardizations(genes, num_of_stocks, day, allocated_funds, handling_fee, returns, securities_transaction_tax, remainder_of_stock):
    fund_standardization = []
    for index in range(num_of_stocks):
        if genes[index] == 1:
            if day ==  1:
                fund_standardization.append(allocated_funds[index] - handling_fee[index])
            elif day > 1:
                fund_standardization.append(returns[index] - handling_fee[index] - securities_transaction_tax[index] + remainder_of_stock[index])
            else:
                print("Funds_standardizations failed.")
        else:
            fund_standardization.append(0)
    # print(fund_standardization)
    return fund_standardization

def pf_funds_standardizations(genes, fund_standardization, remainder_of_pf):
    pf_funds_standardization = np.sum(fund_standardization) + remainder_of_pf
    # print(pf_funds_standardization)
    return pf_funds_standardization

def rois(pf_funds_standardization, initial_fund):
    roi = (pf_funds_standardization - initial_fund) / initial_fund
    return roi

def risks(first_pf_funds_standardization, _pf_funds_standardization):
    std_dev = statistics.stdev([first_pf_funds_standardization, _pf_funds_standardization])
    avg = (first_pf_funds_standardization + _pf_funds_standardization) / 2.0
    print("std dev: " , std_dev)
    print("avg: ", avg)
    risk = std_dev / avg * 100
    return risk

def fitnesses(roi, risk, risk_free_rate):
    fitness = (roi - risk_free_rate) / risk * 100
    return fitness