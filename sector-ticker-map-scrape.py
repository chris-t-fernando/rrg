from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging, sys
import time
import boto3
from selenium.webdriver import Chrome


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# make Selenium not wait until everything loads
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
driver = Chrome(desired_capabilities=caps)

# output csv for now - will pipe it to an eventbridge bus later
f = open("sector-ticker-map.csv", "w")
f.write("sector,ticker\n")

sectorList = {
    'xej': {
        'url': 'https://www.listcorp.com/asx/sectors/energy',
        'tickers': []
    },
    'xmj': { 'url': 'https://www.listcorp.com/asx/sectors/materials',
        'tickers': []
    },
    'xnj': { 'url': 'https://www.listcorp.com/asx/sectors/industrials',
        'tickers': []
    },
    'xdj': { 'url': 'https://www.listcorp.com/asx/sectors/consumer-discretionary',
        'tickers': []
    },
    'xsj': { 'url': 'https://www.listcorp.com/asx/sectors/consumer-staples',
        'tickers': []
    },
    'xhj': { 'url': 'https://www.listcorp.com/asx/sectors/health-care',
        'tickers': []
    },
    'xfj': { 'url': 'https://www.listcorp.com/asx/sectors/financials',
        'tickers': []
    },
    'xij': { 'url': 'https://www.listcorp.com/asx/sectors/information-technology',
        'tickers': []
    },
    'xtj': { 'url': 'https://www.listcorp.com/asx/sectors/communication-services',
        'tickers': []
    },
    'xuj': { 'url': 'https://www.listcorp.com/asx/sectors/utilities',
        'tickers': []
    },
    'xpj': { 'url': 'https://www.listcorp.com/asx/sectors/real-estate',
        'tickers': []
    },
}

with Chrome() as driver:
    try:
        # start the scrape
        for sectorKey in sectorList:
            # get the next page
            driver.get(sectorList[sectorKey]['url'])
            time.sleep(5)
            ticker_elements = driver.find_elements_by_class_name('lcGreyLink')

            # capture the scrape
            for ticker in ticker_elements:
                sectorList[sectorKey]['tickers'].append((ticker.text).replace('ASX:',''))
                f.write(sectorKey+","+(ticker.text).replace('ASX:','')+"\n")

    finally:
        # clean up
        f.close()
        driver.quit()