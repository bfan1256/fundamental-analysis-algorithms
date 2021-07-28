import requests

def get_dcf(symbol):
    request = requests.get('https://financialmodelingprep.com/api/v3/company/discounted-cash-flow/{}'.format(symbol))
    return float(request.json()['dcf']) / float(request.json()['Stock Price'])

def get_ratios(symbol, need_recent=True):
    request = requests.get('https://financialmodelingprep.com/api/v3/financial-ratios/{}'.format(symbol))
    ratios = request.json()['ratios'][0]['investmentValuationRatios']
    if need_recent:
        if '2019' not in request.json()['ratios'][0]['date']:
            return False, 0, 0, 0
    return True, float(ratios['priceEarningsToGrowthRatio']), ratios['dividendYield'], float(ratios['priceFairValue'])

def get_market_cap(symbol):
    request = requests.get('https://financialmodelingprep.com/api/v3/quote/{}'.format(symbol))
    return request.json()[0]['marketCap']



def get_graham_ratios(symbol):
    request = requests.get('https://financialmodelingprep.com/api/v3/company-key-metrics/{}'.format(symbol))
    dcf = requests.get('https://financialmodelingprep.com/api/v3/company/discounted-cash-flow/{}'.format(symbol)).json()
    enterprise = requests.get('https://financialmodelingprep.com/api/v3/enterprise-value/{}'.format(symbol))
    bs = requests.get('https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/{}'.format(symbol)).json()['financials'][0]
    num_shares = float(enterprise.json()['enterpriseValues'][0]['Number of Shares'])
    price = float(dcf['Stock Price'])
    metrics = request.json()['metrics'][0]
    pb = float(metrics['PB ratio'])
    graham_ratio = float(metrics['Graham Number']) / price
    ncav_base = float(bs['Total current assets']) - float(bs['Total liabilities'])
    ncav = price / (ncav_base / num_shares)
    return pb, graham_ratio, ncav

def get_rating(symbol):
    request = requests.get('https://financialmodelingprep.com/api/v3/company/rating/{}'.format(symbol))
    details = request.json()['ratingDetails']
    count = 0
    for detail in details.keys():
        count += float(details[detail]['score'])
    return request.json()['rating']['score'], count / len(details)
