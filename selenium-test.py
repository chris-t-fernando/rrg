from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import boto3

# make Selenium not wait until everthing loads
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
driver = Chrome(desired_capabilities=caps)
#driver = Chrome()

# output csv for now - will pipe it to an RDS instance later
f = open("sectors.csv", "w")

#Or use the context manager
from selenium.webdriver import Chrome
"""
Energy                      xej https://au.investing.com/indices/s-p-asx-200-energy-historical-data
materials                   xmj https://au.investing.com/indices/s-p-asx-200-materials-historical-data
industrials                 xnj https://au.investing.com/indices/s-p-asx-200-industrials-historical-data
consumer discretionary      xdj https://au.investing.com/indices/s-p-asx-200-consumer-disc-historical-data
consumer staples            xsj https://au.investing.com/indices/s-p-asx-200-consumer-staples-historical-data
health care                 xhj https://au.investing.com/indices/s-p-asx-200-health-care-historical-data
financials                  xfj https://au.investing.com/indices/s-p-asx-200-financials-historical-data
information technology      xij https://au.investing.com/indices/s-p-asx-200-info-tech-historical-data                    
Communication Services      xtj https://au.investing.com/indices/s-p-asx-200-telecom-services-historical-data
Utilities                   xuj https://au.investing.com/indices/s-p-asx-200-utilities-historical-data
Real Estate                 xpj https://au.investing.com/indices/s-p-asx200-a-reit-historical-data-historical-data
"""

quoteList = [
    'https://au.investing.com/indices/s-p-asx-200-energy-historical-data',
    'https://au.investing.com/indices/s-p-asx-200-materials-historical-data',
    'https://au.investing.com/indices/s-p-asx-200-industrials-historical-data',
    'https://au.investing.com/indices/s-p-asx-200-consumer-disc-historical-data',
    'https://au.investing.com/indices/s-p-asx-200-consumer-staples-historical-data',
    'https://au.investing.com/indices/s-p-asx-200-health-care-historical-data',
    'https://au.investing.com/indices/s-p-asx-200-financials-historical-data',
    'https://au.investing.com/indices/s-p-asx-200-info-tech-historical-data',
    'https://au.investing.com/indices/s-p-asx-200-telecom-services-historical-data',
    'https://au.investing.com/indices/s-p-asx-200-utilities-historical-data',
    'https://au.investing.com/indices/s-p-asx200-a-reit-historical-data-historical-data'
    ]

with Chrome() as driver:
    try:
        # start with any page, doesn't matter - its just for login
        driver.get('https://au.investing.com/indices/s-p-asx-all-ord-gold-historical-data')
        driver.find_element_by_link_text('Sign In').click()
        
        # grab investing.com credentials from AWS paramter store
        ssm_client = boto3.client('ssm', region_name='us-west-2')
        username=ssm_client.get_parameter(Name='/rrg-creator/investing.com-username', WithDecryption=False).get("Parameter").get("Value")
        password=ssm_client.get_parameter(Name='/rrg-creator/investing.com-password', WithDecryption=True).get("Parameter").get("Value")

        driver.find_element_by_id('loginFormUser_email').send_keys(username)
        # lord god forgive me for hardcoding credentials
        driver.find_element_by_id('loginForm_password').send_keys(password)
        driver.find_element_by_id('loginForm_password').send_keys(Keys.ENTER)
        
        # logged in. start the pull
        for quoteUrl in quoteList:
            driver.get(quoteUrl)
            data_interval_element = driver.find_element_by_id('data_interval')
            data_interval_object = Select(data_interval_element)
            data_interval_object.select_by_visible_text('Weekly')
            
            # wait for weekly data to load
            time.sleep(5)

            # scrape ze table
            table_element =  driver.find_element_by_id('curr_table')
            rows = table_element.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                csvLine = quoteUrl + ","
                cols = row.find_elements(By.TAG_NAME, "td")
                for col in cols:
                    csvLine+=col.text + ","
                    #print(quoteUrl,col.text)
                f.write(csvLine+"\n")

    finally :
        driver.screenshot('screenshot.png')
        f.close()
        driver.quit()