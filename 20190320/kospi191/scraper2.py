import csv
import datetime
# from multiprocessing.pool import ThreadPool
import threading
import queue

THREAD_LEN = 8
que = queue.Queue()

def day_checker(kospi_tickers, index, startdate, enddate):
    prices = []
    with open('./kospi200/' + kospi_tickers[index] + ".csv", 'r') as in_file:
        reader = csv.reader(in_file, delimiter=",")
        for price in reader:
            date = datetime.datetime.strptime(price[0], "%Y-%m-%d")
            if date >= startdate and date <= enddate:
                prices.append(float(price[1]))
    que.put(len(prices))


def price_checker(kospi_tickers, index, startdate, enddate):
    prices = []
    with open('./kospi200/' + kospi_tickers[index] + ".csv", 'r') as in_file:
        reader = csv.reader(in_file, delimiter=",")
        for price in reader:
            date = datetime.datetime.strptime(price[0], "%Y-%m-%d")
            if date >= startdate and date <= enddate:
                prices.append(float(price[1]))
    que.put(prices)


def days(kospi_tickers, startdate, enddate):
    day = []
    num_of_stock = len(kospi_tickers)
    for index in range(len(kospi_tickers)):
        if index < num_of_stock:
            # pool = ThreadPool(processes=16)
            threads = []

            for count in range(THREAD_LEN):
                process = threading.Thread(target=day_checker, args=(kospi_tickers, index, startdate, enddate))
                process.start()
                threads.append(process)

            for process in threads:
                process.join()

            while not que.empty():
                day.append(que.get())

            # async_result = pool.apply_async(day_checker, (kospi_tickers, index, startdate, enddate))
            # day.append(async_result.get())
            # pool.close()
            # pool.join()
    print(day)
    print(len(day))

    return day


def stock_prices(days, kospi_tickers, startdate, enddate):
    all_prices = []
    num_of_stock = len(kospi_tickers)
    for index in range(len(kospi_tickers)):
        if index < num_of_stock:
            # pool = ThreadPool(processes=16)
            # async_result = pool.apply_async(price_checker, (kospi_tickers, index, startdate, enddate))
            # all_prices.append(async_result.get())
            # pool.close()
            # pool.join()

            que = queue.Queue()
            threads = []
            for count in range(THREAD_LEN):
                process = threading.Thread(target=price_checker, args=(kospi_tickers, index, startdate, enddate))
                process.start()
                threads.append(process)

            for process in threads:
                process.join()

            while not que.empty():
                all_prices.append(que.get())

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
    print(stock_price)
    return stock_price