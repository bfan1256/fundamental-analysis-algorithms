import os
import csv
import requests
import numpy as np

from glob import glob
from tqdm import tqdm


from request_functions import *

glob_path = '../stock-tickers/*.txt'

tickers = []
ticker_paths = glob(glob_path)
for path in ticker_paths:
    with open(path) as f:
        reader = csv.DictReader(f, delimiter='|')
        for row in reader:
            # check if it is an ETF
            if row['ETF'] != 'Y':
                tickers.append(row)

def process_ticker(ticker):
    try:
        ticker_symbol = ticker['NASDAQ Symbol']
    except Exception:
        ticker_symbol = ticker['Symbol']
    try:
        cap = get_market_cap(ticker_symbol)
        if cap > 100000000:
            try:
                dcf = get_dcf(ticker_symbol)
                is_recent, peg, dividend, fairvalue = get_ratios(ticker_symbol)
                pb, graham_ratio, ncav = get_graham_ratios(ticker_symbol)
                rating, averaged_rating = get_rating(ticker_symbol)
                if dividend != '' and dividend != '-0' and is_recent != False and fairvalue > 0 and peg > 0:
                    new_fairvalue = -np.log(fairvalue) * 0.2
                    new_peg = -np.log(peg) * 0.1
                    new_pb = -np.log(pb) * 0.4
                    new_ncav = -np.log(ncav) * 0.6
                    final_ticker_rating = dcf * 0.3 + averaged_rating * 0.4 + new_fairvalue + new_peg + new_pb + graham_ratio + new_ncav
                else:
                    final_ticker_rating = 0
                if final_ticker_rating > 0:
                    return [ticker_symbol, final_ticker_rating, dcf, peg, float(dividend), fairvalue, rating]
            except KeyError as e: 
                return

            except ValueError as e:
                return
        else:
            return
    except Exception as e:
        return
final_tickers = []
for ticker in tqdm(tickers):
    res = process_ticker(ticker)
    if res is not None:
        print('Found a Great Stock')
        final_tickers.append(res)

final_tickers.sort(key=lambda x: x[1], reverse=True)

with open('undervalued_good_buys.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Symbol', 'Final Weighted Rating', 'DCF', 'PEG', 'Dividend Payout Ratio', 'P/FV', 'Unweighted Rating'])
    writer.writerows(final_tickers)