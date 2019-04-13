import glob
import os
import datetime

KOSPI_TICKER = []
file_names = [os.path.basename(x) for x in glob.glob('../kospi200/*.csv')]
for file_name in file_names:
    KOSPI_TICKER.append(os.path.splitext(file_name)[0])
NUM_OF_STOCKS = len(KOSPI_TICKER)

