import csv
import datetime
from multiprocessing.pool import ThreadPool

def day_checker(kospi_tickers, index, startdate, enddate):
    prices = []
    with open('./kospi200/' + kospi_tickers[index] + ".csv", 'r') as in_file:
        reader = csv.reader(in_file, delimiter=",")
        for price in reader:
            date = datetime.datetime.strptime(price[0], "%Y-%m-%d")
            if date >= startdate and date <= enddate:
                prices.append(float(price[1]))
    return len(prices)


def price_checker(kospi_tickers, index, startdate, enddate):
    prices = []
    with open('./kospi200/' + kospi_tickers[index] + ".csv", 'r') as in_file:
        reader = csv.reader(in_file, delimiter=",")
        for price in reader:
            date = datetime.datetime.strptime(price[0], "%Y-%m-%d")
            if date >= startdate and date <= enddate:
                prices.append(float(price[1]))
    return prices


def days(kospi_tickers, startdate, enddate):
    day = []
    num_of_stock = len(kospi_tickers)
    for index in range(len(kospi_tickers)):
        if index < num_of_stock:
            pool = ThreadPool(processes=20)
            async_result = pool.apply_async(day_checker, (kospi_tickers, index, startdate, enddate))
            day.append(async_result.get())
    return day


def stock_prices(days, kospi_tickers, startdate, enddate):
    all_prices = []
    num_of_stock = len(kospi_tickers)
    for index in range(len(kospi_tickers)):
        if index < num_of_stock:
            pool = ThreadPool(processes=20)
            async_result = pool.apply_async(price_checker, (kospi_tickers, index, startdate, enddate))
            all_prices.append(async_result.get())

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