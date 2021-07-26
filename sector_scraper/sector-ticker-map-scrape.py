from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import logging, sys
import time
import boto3
import pymysql.cursors
from selenium.webdriver import Chrome


def getSSMParameter(ssm, path, encrypted=False):
    return (
        ssm.get_parameter(Name=path, WithDecryption=encrypted)
        .get("Parameter")
        .get("Value")
    )


logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# make Selenium not wait until everything loads
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
driver = Chrome(desired_capabilities=caps)

sectorList = {
    "xej": {"url": "https://www.listcorp.com/asx/sectors/energy", "codes": []},
    "xmj": {"url": "https://www.listcorp.com/asx/sectors/materials", "codes": []},
    "xnj": {"url": "https://www.listcorp.com/asx/sectors/industrials", "codes": []},
    "xdj": {
        "url": "https://www.listcorp.com/asx/sectors/consumer-discretionary",
        "codes": [],
    },
    "xsj": {
        "url": "https://www.listcorp.com/asx/sectors/consumer-staples",
        "codes": [],
    },
    "xhj": {"url": "https://www.listcorp.com/asx/sectors/health-care", "codes": []},
    "xfj": {"url": "https://www.listcorp.com/asx/sectors/financials", "codes": []},
    "xij": {
        "url": "https://www.listcorp.com/asx/sectors/information-technology",
        "codes": [],
    },
    "xtj": {
        "url": "https://www.listcorp.com/asx/sectors/communication-services",
        "codes": [],
    },
    "xuj": {"url": "https://www.listcorp.com/asx/sectors/utilities", "codes": []},
    "xpj": {"url": "https://www.listcorp.com/asx/sectors/real-estate", "codes": []},
}

with Chrome() as driver:
    try:
        # connect to the database
        ssmClient = boto3.client("ssm")
        connection = pymysql.connect(
            host=getSSMParameter(ssm=ssmClient, path="/rrg-creator/rds-endpoint"),
            user=getSSMParameter(ssm=ssmClient, path="/rrg-creator/rds-user"),
            password=getSSMParameter(
                ssm=ssmClient, path="/rrg-creator/rds-password", encrypted=True
            ),
            database=getSSMParameter(ssm=ssmClient, path="/rrg-creator/rds-database"),
            cursorclass=pymysql.cursors.DictCursor,
        )

        # start the scrape
        for sectorKey in sectorList:
            # get the next page
            driver.get(sectorList[sectorKey]["url"])
            time.sleep(5)

            table_element = driver.find_elements_by_class_name("v-datatable")
            rows = table_element[0].find_elements(By.TAG_NAME, "tr")

            # scrapey scrapey
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) > 0:
                    # got one
                    sectorList[sectorKey]["codes"].append(
                        {
                            "stock_code": (cols[1].text).replace("ASX:", ""),
                            "stock_name": cols[2].text,
                        }
                    )

            logging.info(
                f"Scraped stock codes for sector {sectorKey}.  Found {len(sectorList[sectorKey]['codes'])} stock codes"
            )
    except Exception as e:
        logging.error(
            f"Something went wrong in the scrape.  Has the page changed?  Error: {str(e)}"
        )
    finally:
        # clean up
        driver.quit()

logging.info(f"Finished scraping all sectors.  Beginning stock sync")

with connection:
    with connection.cursor() as cursor:

        newStocks = []
        queryStockCode = "select count(*) from stock where stock_code=%s"

        for sectorKey in sectorList:
            for code in sectorList[sectorKey]["codes"]:
                cursor.execute(queryStockCode, (code["stock_code"]))
                result = cursor.fetchone()
                if result["count(*)"] == 0:
                    # new stock
                    newStocks.append(code)
                    logging.warning(
                        f"New stock found - {code['stock_code']}.  Queueing for insert"
                    )

        insertStockCode = "insert into stock (stock_code, stock_name, sector_code) values (%s, %s, %s)"

        for stock in newStocks:
            try:
                cursor.execute(
                    insertStockCode,
                    (stock["stock_code"], stock["stock_name"], sectorKey),
                )
                logging.warning(
                    f"Successfully inserted new stock {stock['stock_code']}"
                )
            except Exception as e:
                logging.error(
                    f"Failed to insert new stock {stock['stock_code']} with error: {str(e)}"
                )

        connection.commit()
        logging.info(f"Finished sync.")

# TODO: reverse sync, see if records are in DB that aren't in scrape
