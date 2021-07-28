import os
import csv
import requests
import numpy as np

from glob import glob
from tqdm import tqdm

from growth_stock_functions import *

ticker = input('Input Stock Ticker: ')

def process_ticker(ticker_symbol):
    try:
        cap = get_market_cap(ticker_symbol)
        if cap > 75000000:
            try:
                is_recent, turnover, gpm, roa, roe, quick_ratio = get_ratios(ticker_symbol, False)
                gpg, gig, gepsg = company_growth(ticker_symbol)
                rating, averaged_rating = get_rating(ticker_symbol)
                print(turnover)
                final_ticker_rating = turnover * 0.05 + gpm * 0.5 + roa * 0.3 + roe * 0.3 + quick_ratio * 0.05 + (gpg + gig + gepsg) * 0.4 + averaged_rating
                
                
                return [ticker_symbol, final_ticker_rating, gpm, roa, roe, gpg, gig, gepsg, rating]
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
print('Gross Profit Margin: {:.3f}%'.format(result[2] * 100))
print('Return on Asset: {:.3f}%'.format(result[3] * 100))
print('Return on Equity: {:.3f}%'.format(result[4] * 100))
print('Gross Profit Growth: {:.3f}%'.format(result[5] * 100))
print('Net Income Growth: {:.3f}%'.format(result[6] * 100))
print('EPS Growth: {:.3f}%'.format(result[7] * 100))
print('Rating: {}'.format(result[8]))
print('='*15)
print('\n\n')