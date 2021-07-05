from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging, sys
import time
import boto3
from datetime import datetime
from selenium.webdriver import Chrome

# make Selenium not wait until everything loads
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
driver = Chrome(desired_capabilities=caps)

# output csv for now - will pipe it to an eventbridge bus later
f = open("sectors.csv", "w")
f.write("sectorticker,date,close,open,high,low,volume,pct-change\n")

quoteList = {
    'xej': 'https://au.investing.com/indices/s-p-asx-200-energy-historical-data',
    'xmj': 'https://au.investing.com/indices/s-p-asx-200-materials-historical-data',
    'xnj': 'https://au.investing.com/indices/s-p-asx-200-industrials-historical-data',
    'xdj': 'https://au.investing.com/indices/s-p-asx-200-consumer-disc-historical-data',
    'xsj': 'https://au.investing.com/indices/s-p-asx-200-consumer-staples-historical-data',
    'xhj': 'https://au.investing.com/indices/s-p-asx-200-health-care-historical-data',
    'xfj': 'https://au.investing.com/indices/s-p-asx-200-financials-historical-data',
    'xij': 'https://au.investing.com/indices/s-p-asx-200-info-tech-historical-data',
    'xtj': 'https://au.investing.com/indices/s-p-asx-200-telecom-services-historical-data',
    'xuj': 'https://au.investing.com/indices/s-p-asx-200-utilities-historical-data',
    'xpj': 'https://au.investing.com/indices/s-p-asx200-a-reit-historical-data'
}

with Chrome() as driver:
    try:
        # start with any page, doesn't matter - its just for login
        driver.get('https://au.investing.com/indices/s-p-asx-all-ord-gold-historical-data')
        driver.find_element_by_link_text('Sign In').click()
        
        # grab investing.com credentials from AWS paramter store
        ssm_client = boto3.client('ssm', region_name='us-west-2')
        username=ssm_client.get_parameter(Name='/rrg-creator/investing.com-username', WithDecryption=False).get("Parameter").get("Value")
        password=ssm_client.get_parameter(Name='/rrg-creator/investing.com-password', WithDecryption=True).get("Parameter").get("Value")

        # login
        driver.find_element_by_id('loginFormUser_email').send_keys(username)
        driver.find_element_by_id('loginForm_password').send_keys(password)
        driver.find_element_by_id('loginForm_password').send_keys(Keys.ENTER)
        
        # logged in. start the scrape
        for quoteKey in quoteList:
            # get the next page
            driver.get(quoteList[quoteKey])

            # set the data interval to weekly
            data_interval_element = driver.find_element_by_id('data_interval')
            data_interval_object = Select(data_interval_element)
            data_interval_object.select_by_visible_text('Weekly')
            
            # wait for weekly data to load
            time.sleep(5)

            # yarrr
            table_element =  driver.find_element_by_id('curr_table')
            rows = table_element.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                csvLine = quoteKey + ","
                cols = row.find_elements(By.TAG_NAME, "td")
                
                # expect 7 columns
                if len(cols) == 7:
                    colCount = 0
                    for col in cols:
                        # change format of date string in position 0.  Probably a sexier way of doing this
                        if colCount == 0:
                            date_time_obj = datetime.strptime(col.text, "%b %d, %Y")
                            csvLine+= date_time_obj.strftime('%Y-%m-%d') + ","
                            colCount += 1
                        else: 
                            # strip any errant , in the string
                            csvLine+=col.text.replace(',','') + ","

                        #print(quoteUrl,col.text)
                    f.write(csvLine+"\n")
                else:
                    logging.debug("Found less than 7 elements in this row, dropping.  Row was: : %d", row)

    finally:
        # clean up
        f.close()
        driver.quit()