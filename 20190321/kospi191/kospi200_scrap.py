from bs4 import BeautifulSoup
import re
import requests
import pandas_datareader.data as web
import glob
import pandas as pd

BaseUrl = 'http://finance.naver.com/sise/entryJongmok.nhn?&page='
Portal = 'yahoo'
Code = '.KS'
def kospi_data(StartDate, EndDate):
    for i in range(1,22,1):
        try:
            url = BaseUrl + str(i)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            items = soup.find_all('td', {'class':'ctg'})
            count = 1
            for item in items:

                print(i, "th page", count, "th element is now updating")
                txt = item.a.get('href')
                k = re.search('[\d]+', txt)
                if k:
                    ticker = k.group() + Code
                    name = item.text
                    # data = ticker, name

                    gs = web.DataReader(ticker, Portal, StartDate, EndDate)
                    gs['Adj Close'].to_csv('./kospi200/{}.csv'.format(ticker))
                    print('{}.csv is saved'.format(ticker))
                count += 1

        except:
            print("failed loading kospi data")

        finally:
            pass

def fix_data(StartDate, EndDate):
    file_list = glob.glob('./kospi200/*.csv'.format('kospi200'))

    six_digit = re.compile('\d{6}')
    for file_name in file_list:
        file = pd.read_csv(file_name)
        if file.empty:
            print("file {} is empty".format(file_name))
            ticker = six_digit.findall(file_name[0])
            print("now updating…")
            print(ticker)
            _ticker = ticker + [Code]['market' == 'kospi200']
            tmp_df = web.DataReader(ticker, Portal, StartDate, EndDate)
            tmp_df.to_csv(file_name)
        else:
            print("file {} is not empty".format(file_name))

