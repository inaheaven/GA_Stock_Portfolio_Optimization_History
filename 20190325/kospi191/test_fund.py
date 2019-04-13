from settings import *

import fund_standardization


def test_best_population(kospi_ticker, best_chromosome, test_day_list, test_stock_price_list, year, month, monthly_best_file_name):
    test_genes = best_chromosome.get_genes()
    # print("test_genes", test_genes)
    test_days = test_day_list
    # print("test_days", test_days)
    test_stock_prices = test_stock_price_list
    # print("test_stock_prices", test_stock_prices)
    test_num_of_stocks = best_chromosome.get_num_of_stocks()
    # print("test_num_of_stocks", test_num_of_stocks)
    test_num_of_stocks = len(kospi_ticker)
    test_num_of_selected_stocks = fund_standardization.num_of_selected_stocks(test_genes, test_num_of_stocks)
    test_allocated_fund_amount = 0
    test_remainder_of_pf = 0
    if test_num_of_selected_stocks != 0:
        test_allocated_fund_amount = INITIAL_FUNDS // test_num_of_selected_stocks
        test_remainder_of_pf = 0
    else:
        test_allocated_fund_amount = 0
        test_remainder_of_pf = INITIAL_FUNDS

    test_allocated_fund = fund_standardization.allocated_funds(test_genes, test_allocated_fund_amount, test_num_of_stocks)
    # print("_allocated_fund", test_allocated_fund )
    test_remainder_of_pf = fund_standardization.remainder_of_pfs(INITIAL_FUNDS, test_allocated_fund_amount, test_num_of_selected_stocks)
    # print("test_days", test_days)
    # print("_stock_price", test_stock_prices)
    test_share = fund_standardization.shares(test_genes, test_num_of_stocks, test_allocated_fund, test_stock_prices, FEE_RATE)
    # print("_share", test_share)
    test_handling_fee = fund_standardization.handling_fees(test_genes, test_days, test_num_of_stocks, test_share, test_stock_prices, FEE_RATE)
    # print("_handling_fee", test_handling_fee)
    test_remainder_of_stock = fund_standardization.remainder_of_stocks(test_genes, test_num_of_stocks, test_allocated_fund, test_stock_prices, test_share, test_handling_fee)
    # print("_remainder_of_stock", test_remainder_of_stock)
    test_return = fund_standardization.returns(test_genes, test_days, test_num_of_stocks, test_share, test_stock_prices)
    # print("_return", test_return)
    test_securities_transaction_tax = fund_standardization.securities_transaction_taxes(test_genes, test_days, test_num_of_stocks, test_share, test_stock_prices, TAX_RATE)
    # print("_securities_transaction_tax", test_securities_transaction_tax)
    test_funds_standardization = fund_standardization.funds_standardizations(test_genes, test_num_of_stocks, test_days, test_allocated_fund, test_handling_fee, test_return, test_securities_transaction_tax, test_remainder_of_stock)
    # print("_funds_standardization", test_funds_standardization)
    test_pf_funds_standardization = fund_standardization.pf_funds_standardizations(test_days, test_num_of_stocks, test_funds_standardization, test_remainder_of_pf)
    # print("_pf_funds_standardization", test_pf_funds_standardization )
    test_roi = fund_standardization.rois(test_pf_funds_standardization, INITIAL_FUNDS)
    test_risk = fund_standardization.risks(test_days, test_pf_funds_standardization)
    test_fitness = fund_standardization.fitnesses(test_roi, test_risk, RISK_FREE_RATE)

    for count in range(650):
        print("*", end="")
    print()
    print("_roi", test_roi)
    print("_risk", test_risk)
    print("Fitness: ", test_fitness)

    for count in range(650):
        print("*", end="")
    print()
