import os
import csv
import requests
import numpy as np

from glob import glob
from tqdm import tqdm

import multiprocessing as mp

from request_functions import *

ticker = input('Input Stock Ticker: ')

def process_ticker(ticker_symbol):
    try:
        cap = get_market_cap(ticker_symbol)
        if cap > 75000000:
            try:
                dcf = get_dcf(ticker_symbol)
                is_recent, peg, dividend, fairvalue = get_ratios(ticker_symbol, False)
                rating, averaged_rating = get_rating(ticker_symbol)
                if dividend == '' or dividend == '-0':
                    dividend = 0
                if fairvalue > 0 and peg > 0:
                    new_fairvalue = -np.log(fairvalue) * 0.2
                    new_peg = -np.log(peg) * 0.1
                    final_ticker_rating = dcf * 0.3 + averaged_rating * 0.4 + new_fairvalue + new_peg
                else:
                    final_ticker_rating = 0
                if final_ticker_rating > 0:
                    return [ticker_symbol, final_ticker_rating, dcf, peg, float(dividend), fairvalue, rating]
            except KeyError as e: 
                print(e)
                return

            except ValueError as e:
                print(e)
                return
        else:
            return
    except Exception as e:
        print(e)
        return


result = process_ticker(ticker)
print('\n\n')
print('='*15)
print('Ticker: {}'.format(result[0]))
print('Final Ticker Rating: {:.3f}'.format(result[1]))
print('DCF/P: {:.3f}'.format(result[2]))
print('PEG: {:.3f}'.format(result[3]))
print('Dividend Payout Ratio: {:.3f}%'.format(result[4] * 100))
print('P/FV: {:.3f}'.format(result[5]))
print('Unweighted Rating: {}'.format(result[6]))
print('='*15)
print('\n\n')