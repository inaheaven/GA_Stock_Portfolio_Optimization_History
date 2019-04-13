import csv
import datetime


def day_checker(kospi_tickers, index, start_date, end_date):
    prices = []
    with open('../kospi200/' + kospi_tickers[index] + ".csv", 'r') as in_file:
        reader = csv.reader(in_file, delimiter=",")
        for price in reader:
            date = datetime.datetime.strptime(price[0], "%Y-%m-%d")
            if date >= start_date and date <= end_date:
                prices.append(float(price[1]))
    return len(prices)


def price_checker(kospi_tickers, index, start_date, end_date):
    prices = []
    with open('../kospi200/' + kospi_tickers[index] + ".csv", 'r') as in_file:
        reader = csv.reader(in_file, delimiter=",")
        for price in reader:
            date = datetime.datetime.strptime(price[0], "%Y-%m-%d")
            if date >= start_date and date <= end_date:
                prices.append(float(price[1]))
    return prices


def days(kospi_tickers, start_date, end_date):
    day = []
    num_of_stock = len(kospi_tickers)
    for index in range(len(kospi_tickers)):
        if index < num_of_stock:
            day.append(day_checker(kospi_tickers, index, start_date, end_date))

    return day


def stock_prices(days, kospi_tickers, start_date, end_date):
    all_prices = []
    num_of_stock = len(kospi_tickers)
    for index in range(len(kospi_tickers)):
        if index < num_of_stock:
            all_prices.append(price_checker(kospi_tickers, index, start_date, end_date))

    stock_price = []
    last_day = 1
    for index in range(len(kospi_tickers)):
        prices = []
        if days[index] != 0:
            last_day = days[index]
            for day in range(days[index]):
                prices.append(all_prices[index][day])
        else:
            for day in range(last_day):
                prices.append(0)
        stock_price.append(prices)
    return stock_price
