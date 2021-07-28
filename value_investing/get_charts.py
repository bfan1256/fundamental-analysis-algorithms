import csv
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
sns.set('talk')
n = input('Number of Charts: ')
with open('./final_data/growth_good_buys_filtered.csv') as f:
    reader = csv.reader(f)
    data = []
    for row in reader:
        data.append(row)
for row in tqdm(data[1:int(n) + 1]): 
    ticker = yf.Ticker(row[0])
    history = ticker.history(period='max')
    plt.figure(figsize=(30, 16))
    ax = sns.lineplot(x=history.index, y='Close', data=history)
    ax.set_title('Closing Prices for {}'.format(row[0]))
    plt.savefig('stock_charts/{}.png'.format(row[0]))
    plt.clf()
    plt.close()