import os
import csv
import requests
import numpy as np

from glob import glob
from tqdm import tqdm

from growth_stock_functions import *


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

final_tickers = []


def process_ticker(ticker_symbol):
    try:
        cap = get_market_cap(ticker_symbol)
        if cap > 20000000:
            try:
                is_recent, turnover, gpm, roa, roe, quick_ratio = get_ratios(ticker_symbol, False)
                gpg, gig, gepsg = company_growth(ticker_symbol)
                rating, averaged_rating = get_rating(ticker_symbol)
                
                final_ticker_rating = turnover * 0.05 + gpm * 0.5 + roa * 0.3 + roe * 0.3 + quick_ratio * 0.05 + (gpg + gig + gepsg) * 0.4 + averaged_rating
                
                
                return [ticker_symbol, final_ticker_rating, gpm, roa, roe, gpg, gig, gepsg, rating]
            except KeyError as e: 
                return

            except ValueError as e:
                return
        else:
            return
    except Exception as e:
        return


for ticker in tqdm(tickers):
    try:
        ticker_symbol = ticker['NASDAQ Symbol']
    except Exception:
        ticker_symbol = ticker['Symbol']
    res = process_ticker(ticker_symbol)
    if res is not None:
        final_tickers.append(res)

final_tickers.sort(key=lambda x: x[1], reverse=True)

with open('growth_good_buys.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Symbol', 'Final Weighted Rating', 'GPM', 'ROA', 'ROE', 'Gross Profit Growth', 'Net Income Growth', 'EPS Growth', 'Unweighted Rating'])
    writer.writerows(final_tickers)
