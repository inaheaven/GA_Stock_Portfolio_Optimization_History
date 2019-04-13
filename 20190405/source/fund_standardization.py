import numpy as np
from settings_rates import *

def num_of_selected_stocks(genes, num_of_stock):
    num_of_selected_stock = 0
    for index in range(num_of_stock):
        if genes[index] == 1:
            num_of_selected_stock += 1
    return num_of_selected_stock


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


def shares(genes, num_of_stocks, allocated_funds, stock_price, rate):
    share = []
    for index in range(num_of_stocks):
        if genes[index] == 1 and stock_price[index][0] != 0:
            share.append(allocated_funds[index] // (stock_price[index][0] + stock_price[index][0] * rate))
        elif genes[index] == 1 and stock_price[index][0] == 0:
            share.append(0)
        else:
            share.append(0)
    return share


def handling_fees(genes, days, num_of_stocks, share, stock_price, rate):
    handling_fee = []
    for index in range(num_of_stocks):
        fee = []
        for day in range(days[index]):
            if genes[index] == 1:
                fee.append(share[index] * stock_price[index][day] * rate)
            else:
                fee.append(0)
        handling_fee.append(fee)
    return handling_fee


def remainder_of_stocks(genes, num_of_stocks, allocated_funds, stock_price, share, handling_fee):
    remainder = []
    for index in range(num_of_stocks):
        if genes[index] == 1 and stock_price[index][0] != 0:
            remainder.append(np.floor(allocated_funds[index] - (stock_price[index][0] * share[index]) - handling_fee[index][0]))
        elif genes[index] == 1 and stock_price[index][0] == 0:
            remainder.append(0)
        else:
            remainder.append(0)
    return remainder


def returns(genes, days, num_of_stocks, share, stock_price):
    cash_values = []
    for index in range(num_of_stocks):
        cash = []
        for day in range(days[index]):
            if genes[index] == 1:
                cash.append(stock_price[index][day] * share[index])
            else:
                cash.append(0)
        cash_values.append(cash)
    return cash_values


def securities_transaction_taxes(genes, days, num_of_stocks, share, stock_price, rate):
    taxes = []
    for index in range(num_of_stocks):
        tax = []
        for day in range(days[index]):
            if genes[index] == 1:
                tax.append(share[index] * stock_price[index][day] * rate)
            else:
                tax.append(0)
        taxes.append(tax)
    return taxes


def funds_standardizations(genes, num_of_stocks, days, allocated_funds, handling_fee, returns, securities_transaction_tax, remainder_of_stock):
    funds_standardization = []
    last_day = 1
    for index in range(num_of_stocks):
        fund_standardization = []
        if days[index] != 0:
            last_day = days[index]
            for day in range(days[index]):
                if genes[index] == 1:
                    if day == 0:
                        fund_standardization.append(allocated_funds[index] - handling_fee[index][day])
                    elif day > 0:
                        fund_standardization.append(returns[index][day] - handling_fee[index][day] - securities_transaction_tax[index][day] + remainder_of_stock[index])
                    else:
                        print("Funds Standardizations Failed.")
                else:
                    fund_standardization.append(0)
        else:
            for day in range(last_day):
                fund_standardization.append(0)

        funds_standardization.append(fund_standardization)
    return funds_standardization


def pf_funds_standardizations(days, num_of_stocks, fund_standardization, remainder_of_pf):
    pf_funds_standardization = []
    count = 0
    for day in range(days[count]):
        pf_fund_standardization = 0
        for index in range (num_of_stocks):
            if days[index] > day:
                pf_fund_standardization += fund_standardization[index][day]
        pf_funds_standardization.append(np.round(pf_fund_standardization, 2) + remainder_of_pf)
        count += 1
    # print(len(pf_funds_standardization), ":", pf_funds_standardization)
    return pf_funds_standardization


def rois(pf_funds_standardization, initial_fund):
    # print(pf_funds_standardization)
    # print(len(pf_funds_standardization))
    roi = (pf_funds_standardization[len(pf_funds_standardization)-1] - initial_fund) / initial_fund * 100
    return roi


def risks(days, _pf_funds_standardization):
    max_day = 1
    for day in days:
        if day > max_day:
            max_day = day
    if len(_pf_funds_standardization) > 1:
        std_dev = np.round(np.std(_pf_funds_standardization), 2)
        # print("std dev: ", std_dev)
        avg = np.sum(_pf_funds_standardization) / max_day
        # print("avg", avg)
        if avg != 0:
            risk = std_dev / avg * 100
        else:
            risk = -9999999
    else:
        risk = -9999999
    return risk


def fitnesses(roi, risk, risk_free_rate):
    if risk != 0:
        fitness = (roi - risk_free_rate) / (risk * risk) # more weights on risk to avoid risky selections.
    else:
        fitness = -9999999
    return fitness
