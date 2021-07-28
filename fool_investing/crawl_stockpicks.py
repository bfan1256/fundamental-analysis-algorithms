import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm


def create_driver():
    driver = webdriver.Chrome('./chromedriver')
    return driver

all_open_recommendations = []
def main():
    driver = create_driver()
    driver.get('https://www.fool.com/secure/login.aspx?redirectURL=https%3A//www.fool.com/')
    res = input('Please Login, Press Any Key When Finished')
    driver.get('https://www.fool.com/premium/stock-advisor/recommendations/all/')
    table_body = driver.find_element_by_css_selector('table.table.tablesorter tbody')
    recommendations = table_body.find_elements_by_css_selector('tr')
    for recommendation in tqdm(recommendations):
        ticker = recommendation.find_element_by_css_selector('td.ticker').text
        cells = recommendation.find_elements_by_css_selector('td')
        date = cells[0].text
        try:
            cells[1].find_element_by_css_selector('span.closed-date')
            continue
        except Exception:
            all_open_recommendations.append({
                'ticker': ticker,
                'date_recommended': date
            })
    
    with open('recommendations.json', 'w') as f:
        json.dump(all_open_recommendations, f, indent=4)

if __name__ == "__main__":
    main()