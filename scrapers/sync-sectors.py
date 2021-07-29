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

# from selenium.webdriver.remote.remote_connection import logging as sellogging

# sellogging.setLevel(logging.ERROR)


def getSSMParameter(ssm, path, encrypted=False):
    return (
        ssm.get_parameter(Name=path, WithDecryption=encrypted)
        .get("Parameter")
        .get("Value")
    )


logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
logging.debug("asasdasd")

# logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# make Selenium not wait until everything loads
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "eager"
driver = Chrome(desired_capabilities=caps)


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
        logging.info(f"Connected to database")

        # get sectors, create result structure
        sectorList = {}

        driver.get("https://www.listcorp.com/asx/sectors/")
        time.sleep(5)

        links = driver.find_elements_by_class_name("lcGreyPermanentLink")
        for link in links:
            if link.tag_name == "a":
                if link.get_attribute("href") != None:
                    thisSectorCode = str(link.text[-4:-1]).lower()
                    thisSectorUrl = link.get_attribute("href")
                    thisSectorName = link.get_attribute("title")

                    sectorList[thisSectorCode] = {
                        "url": thisSectorUrl,
                        "codes": [],
                        "name": thisSectorName,
                    }

        #        sectorList = {
        #            "xej": {"url": "https://www.listcorp.com/asx/sectors/energy", "codes": []},
        #            "xmj": {
        #                "url": "https://www.listcorp.com/asx/sectors/materials",
        #                "codes": [],
        #            },
        #        }

        logging.warning(f"Got list of sectors.  Found {len(sectorList)}")

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
                            "stock_code": (cols[1].text).replace("ASX:", "").lower(),
                            "stock_name": cols[2].text,
                        }
                    )

            logging.warning(
                f"Scraped stock codes for sector {sectorKey}.  Found {len(sectorList[sectorKey]['codes'])} stock codes"
            )
    except Exception as e:
        logging.error(
            f"Something went wrong in the scrape.  Has the page changed?  Error: {str(e)}"
        )
        raise
    finally:
        # clean up
        driver.quit()
        logging.warning(f"Finished scrape, shut down Chrome")

    logging.warning(f"Finished scraping all sectors.  Beginning stock sync")


# TODO: reverse sync, see if records are in DB that aren't in scrape
with connection:
    with connection.cursor() as cursor:

        # make sure all of the sectors exist
        querySector = "select sector_code from sector"
        cursor.execute(querySector)

        dbSectors = []
        for result in cursor.fetchall():
            dbSectors.append(result["sector_code"])

        newSectors = []
        for scrapedSector in sectorList.keys():
            if scrapedSector not in dbSectors:
                # new sector code
                newSectors.append(
                    (
                        scrapedSector,
                        sectorList[scrapedSector]["name"],
                    )
                )

        logging.warning(f"Got all sectors.  Found {len(newSectors)} new sectors")
        try:
            for newSector in newSectors:
                insertSector = (
                    "insert into sector (sector_code, sector_name) values (%s, %s)"
                )
                cursor.execute(insertSector, newSector)
                logging.warning(f"Successfully inserted new sector_code {newSector[0]}")
        except Exception as e:
            logging.error(
                f"Unable to insert new sector_code {newSector[0]}.  Error: {str(e)}"
            )
            exit()
        connection.commit()

        # move on to syncing stocks
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
                        f"New stock queued for insert: {code['stock_code']}"
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
                    f"Failed to insert new stock {stock['stock_code']} to {sectorKey} with error: {str(e)}"
                )

        connection.commit()
        logging.warning(f"Finished sync.")
