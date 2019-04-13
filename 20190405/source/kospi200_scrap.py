from bs4 import BeautifulSoup
import re
import requests
import pandas_datareader.data as web
import csv

BASE_URL = 'http://finance.naver.com/sise/entryJongmok.nhn?&page='
PORTAL = 'yahoo'
CODE = '.KS'


def kospi_data(start_date, end_date):
    try:
        for i in range(1, 22, 1):
            url = BASE_URL + str(i)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            items = soup.find_all('td', {'class': 'ctg'})

            for item in items:
                txt = item.a.get('href')
                k = re.search('[\d]+', txt)
                if k:
                    ticker = k.group() + CODE
                    name = item.text
                    ticker_name = ticker, name
                    gs = web.DataReader(ticker, PORTAL, start_date, end_date)
                    gs['Adj Close'].to_csv('../kospi200/{}.csv'.format(ticker))
                with open('../source/KOSPI200.csv', 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(ticker_name)

    except Exception as e:
        print('Errors While Scraping KOSPI Data: ' + str(e))

    finally:
        temp_for_sort = []
        with open('../source/KOSPI200.csv', 'r') as in_file:
            for sort_line in in_file:
                temp_for_sort.append(sort_line)
        temp_for_sort.sort()
        with open('../source/KOSPI200.csv', 'w') as out_file:
            seen = set()
            for line in temp_for_sort:
                if line in seen:
                    continue
                else:
                    if not line == None:
                        seen.add(line)
                sorted(seen)
                out_file.write(line)

    print("Scraping KOSPI Data Completed.")

# def fix_data(start_date, end_date):
#     file_list = glob.glob('./kospi200/*.csv'.format('kospi200'))
#     six_digit = re.compile('\d{6}')
#     for file_name in file_list:
#         file = pd.read_csv(file_name)
#         if file.empty:
#             print("file {} is empty".format(file_name))
#             ticker = six_digit.findall(file_name[0])
#             print("now updating…")
#             print(ticker)
#             _ticker = ticker + [CODE]['market' == 'kospi200']
#             tmp_df = web.DataReader(ticker, PORTAL, start_date, end_date)
#             tmp_df.to_csv(file_name)
#         else:
#             print("file {} is not empty".format(file_name))
#

