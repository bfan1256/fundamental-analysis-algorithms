import requests


def get_ratios(symbol, need_recent=True):
    request = requests.get('https://financialmodelingprep.com/api/v3/financial-ratios/{}'.format(symbol))
    ratios = request.json()['ratios'][0]
    if need_recent:
        if '2019' not in request.json()['ratios'][0]['date']:
            return False, 0, 0, 0
    return True, float(ratios['investmentValuationRatios']['priceEarningsToGrowthRatio']), float(ratios['investmentValuationRatios']['receivablesTurnover']), float(ratios['profitabilityIndicatorRatios']['grossProfitMargin']), float(ratios['profitabilityIndicatorRatios']['returnOnAssets']), float(ratios['profitabilityIndicatorRatios']['returnOnEquity']), float(ratios['liquidityMeasurementRatios']['quickRatio'])

def get_market_cap(symbol):
    request = requests.get('https://financialmodelingprep.com/api/v3/quote/{}'.format(symbol))
    return float(request.json()[0]['marketCap'])

def company_growth(symbol):
    request = requests.get('https://financialmodelingprep.com/api/v3/financial-statement-growth/{}'.format(symbol))
    return float(request.json()['growth'][0]['Gross Profit Growth']), float(request.json()['growth'][0]['Net Income Growth']), float(request.json()['growth'][0]['EPS Growth'])

def get_rating(symbol):
    request = requests.get('https://financialmodelingprep.com/api/v3/company/rating/{}'.format(symbol))
    details = request.json()['ratingDetails']
    count = 0
    for detail in details.keys():
        if detail in ['ROA', 'ROE']:
            count += float(details[detail]['score']) * 1.5
        else:
            count += float(details[detail]['score'])
    return request.json()['rating']['score'], count / len(details)
