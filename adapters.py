from typing import List, Dict
import services as i
import logging, sys
import csv
import boto3
import mysql.connector

logging.basicConfig(stream=sys.stderr, level=logging.INFO)


# can only reference tuples by position index, not by column name - annoying!
# shamelessly stolen from https://kadler.io/2018/01/08/fetching-python-database-cursors-by-column-name.html#
class CursorByName():
    def __init__(self, cursor):
        self._cursor = cursor
    
    def __iter__(self):
        return self

    def __next__(self):
        row = self._cursor.__next__()
        return { description[0]: row[col] for col, description in enumerate(self._cursor.description) }

# handler for pulling config from SSM
def getSSMParameter(ssm, parameterPath, encryptionOption=False):
    return ssm.get_parameter(Name=parameterPath, WithDecryption=encryptionOption).get('Parameter').get('Value')




# need to rewrite this so that the rest api calls a storage object, which in turn calls another object that does the 
# reading from json or csv or whatever, and then this object below just loads that data into the services objects
class CSVStorage(i.sectorStorage):
    def __init__(self):
        pass

    # used for setting up _storage for searching by a SECTOR ticker (as opposed to searching by company)
    # reads CSV contents and populates it into the _storage variable
    # the _storage variable is set up like this:
    # _storage[someSectorTicker] which is a sectorTicker object defined in services.py
    # then historical quotes are populated by calling .addQuote against each sectorTicker object, which in turn
    # just adds them to the quote Dict in that object
    def sectorRead(self):
        # read from CSV
        self._storage: Dict[i.sectorTicker] = {}
        tickerCount = 0

        # read the CSV
        with open('sector-ticker-map.csv', newline='') as csvfile:
            mapReader = csv.DictReader(csvfile, delimiter=',')

            for row in mapReader:
                # if the sector key hasn't been instantiated, create it
                sector = row['sector'].lower()
                if sector not in self._storage:
                    self._storage[sector] = i.sectorTicker(sectorTickerCode=sector)
                
                # add the tickers that belong to this sector
                ticker = row['ticker'].lower()
                # adds the ticker to the ticker List variable inside this sectorTicker object
                self._storage[sector].addTicker(ticker)
                tickerCount += 1

        logging.info('Finished loading sector:ticker map. Total sectors is ' +  str(len(self._storage)) + ', total tickers is ' + str(tickerCount))

        # now populate the historical quotes against each of those sectors
        # populates the quotes Dict in each sectorTicker object
        with open('sectors.csv', newline='') as csvfile:
            tickerReader = csv.DictReader(csvfile, delimiter=',')
            quoteCount = 0
            for row in tickerReader:
                # todo - I forgot to add 'offer'.  I don't think I'll use it but noting just in case.  hardcoding to 0 because I'm lazy
                self._storage[row['sectorticker']].addQuote(row['date'], row['open'], row['high'], row['low'], 0, row['close'], row['volume'])
                quoteCount += 1
        
        logging.info('Finished loading ' + str(quoteCount) + ' sector quotes')


    # the filtering happens in adapters but I don't know if I agree with this?  Shouldn't it be done in services?
    # 1. sectors - list of the sectors
    # 2. sectors/{sector} - details of that sector, including all of the tickers belonging to it, and a list of dates we have quotes for it
    # sector
    #  -tickers
    #  -quote dates
    def get_sectors(self, filters: i.sectorFilter) -> List[i.sectorTicker]:
        result = {}

        # loop through all sectors in our storage
        for allSector in self._storage:
            # loop through all sectors in the filter
            for searchSectorList in filters:
                # position 0 is the key name for some reason
                for searchSector in searchSectorList[1]:
                    # if this sector matches this sector filter, or if we're looking for all sectors
                    if ( searchSector == allSector ) or ( searchSector == "*"):
                        # if the results object doesn't already have this sector defined, we need to instantiate it
                        if searchSector not in result:
                           result[allSector] = {}
                           result[allSector]['tickers'] = []
                           result[allSector]['quotes'] = []
                        # stick it on
                        result[allSector]['tickers'] = self._storage[allSector].getTickers()
                        result[allSector]['quotes'] = self._storage[allSector].getQuoteList()

        #logging.info(result)
        return result

    # used for setting up _storage for searches by an individual company's stock's ticker as opposed to search by sector
    # reads CSV contents and populates it into the _storage variable
    # the _storage variable is set up like this:
    # _storage[aStockTicker] which is a ticker object defined in services.py
    # then historical quotes are populated by calling .addQuote against each ticker object, which in turn
    # just adds them to the quote List in that object
    def tickerRead(self):
        # read from CSV
        self._storage: Dict[i.ticker] = {}
        sectors = {}

        with open('sector-ticker-map.csv', newline='') as csvfile:
            mapReader = csv.DictReader(csvfile, delimiter=',')

            for row in mapReader:
                # if the sector key doesn't exist, create it
                ticker = row['ticker'].lower()
                sector = row['sector'].lower()

                if ticker not in self._storage:
                    self._storage[ticker] = i.ticker(tickerCode=ticker, sectorCode=sector)
                
                self._storage[ticker].addQuote('2021-06-01', 0 , 1, 2, 3, 4, 5)
                # i don't think this line does anything any more....
                sectors[sector] = ""

        logging.info('Finished loading ticker:sector map. Total tickers is ' + str(len(self._storage)) + ' across ' + str(len(sectors)) + ' sectors with only stub quotes')

        # now populate the historical quotes
        # I don't have this data yet...
        # for later
        # self._storage[row['sectorticker']].addQuote(row['date'], row['open'], row['high'], row['low'], 0, row['close'], row['volume'])


    # the filtering happens in adapters but I don't know if I agree with this?  Shouldn't it be done in services?
    # 3. tickers - list of the tickers
    # 4. tickers/{ticker} - details of a specific ticker, including the sector it belongs to, and a list of dates we have quotes for it
    # ticker
    #  -sector
    #  -quote dates
    def get_tickers(self, filters: i.tickerFilter) -> List[i.ticker]:
        result = {}
        # loop through the tickers in our storage structure
        for allTicker in self._storage:
            # loop through the filters
            for searchTickerList in filters.tickers:
                if ( searchTickerList == allTicker ) or ( searchTickerList == "*" ):
                    result[allTicker] = {}
                    result[allTicker]['sector'] = self._storage[allTicker].getSector()
                    # call getQuoteList with a filter on it
                    result[allTicker]['quotes'] = self._storage[allTicker].getQuoteList()

                #for searchTicker in searchTickerList: 
                #    if ( searchTicker == allTicker ) or ( searchTicker == "*" ):
                #        result[allTicker] = {}
                #        result[allTicker]['sector'] = self._storage[allTicker].getSector()
                #        # call getQuoteList with a filter on it
                #        result[allTicker]['quotes'] = self._storage[allTicker].getQuoteList()
        #logging.info(result)
        
        return result





# need to rewrite this so that the rest api calls a storage object, which in turn calls another object that does the 
# reading from json or csv or whatever, and then this object below just loads that data into the services objects
class MySQLStorage(i.sectorStorage):
    _mydb: mysql.connector
    _mycusor: mysql.connector

    def __init__(self):
        # set up boto SSM
        ssmClient = boto3.client('ssm')

        # get queue endpoint
        queueUrl = getSSMParameter(ssmClient, '/rrg-creator/queue-endpoint')
        queueClient = boto3.client('sqs')

        logging.info('Connecting to DB') 

        # set up MySQL
        self._mydb = mysql.connector.connect(
            host = getSSMParameter(ssmClient, '/rrg-creator/rds-endpoint'),
            user = getSSMParameter(ssmClient, '/rrg-creator/rds-user'),
            password = getSSMParameter(ssmClient, '/rrg-creator/rds-password', True),
            database = getSSMParameter(ssmClient, '/rrg-creator/rds-database')
        )

        logging.info('Connected to DB')

        self._mycursor = self._mydb.cursor(buffered=True)


    # used for setting up _storage for searching by a SECTOR ticker (as opposed to searching by company)
    # reads DB contents and populates it into the _storage variable
    # the _storage variable is set up like this:
    # _storage[someSectorTicker] which is a sectorTicker object defined in services.py
    # then historical quotes are populated by calling .addQuote against each sectorTicker object, which in turn
    # just adds them to the quote Dict in that object
    def sectorRead(self):
        # read from RDS
        self._storage: Dict[i.sectorTicker] = {}
        tickerCount = 0

        # query the DB
        self._mycursor.execute('SELECT stock_code, sector_code FROM stock')

        # now get the weekly quotes for each
        for row in CursorByName(self._mycursor):
            #if row['last_quote'] == None:
            if row['sector_code'] not in self._storage:
                self._storage[row['sector_code']] = i.sectorTicker(sectorTickerCode=row['sector_code'])
            
            self._storage[row['sector_code']].addTicker(row['stock_code'])

        logging.info('Finished loading sector:ticker map. Total sectors is %s, total tickers is %s', str(len(self._storage)),  str(tickerCount))



        # now populate the historical quotes against each of those sectors
        # populates the quotes Dict in each sectorTicker object
        self._mycursor.execute('SELECT quote_date, sector_code, open_price, high_price, low_price, close_price, volume FROM weekly_sector_quotes')
        for row in CursorByName(self._mycursor):
            self._storage[row['sector_code']].addQuote(row['quote_date'], row['open_price'], row['high_price'], row['low_price'], 0, row['close_price'], row['volume'])
        
        logging.info('Finished loading %s sector quotes', str(tickerCount))


    # the filtering happens in adapters but I don't know if I agree with this?  Shouldn't it be done in services?
    # 1. sectors - list of the sectors
    # 2. sectors/{sector} - details of that sector, including all of the tickers belonging to it, and a list of dates we have quotes for it
    # sector
    #  -tickers
    #  -quote dates
    # todo: just query the database instead of holding everything in memory
    def get_sectors(self, filters: i.sectorFilter) -> List[i.sectorTicker]:
        result = {}

        # loop through all sectors in our storage
        for allSector in self._storage:
            # loop through all sectors in the filter
            for searchSectorList in filters:
                # position 0 is the key name for some reason
                for searchSector in searchSectorList[1]:
                    # if this sector matches this sector filter, or if we're looking for all sectors
                    if ( searchSector == allSector ) or ( searchSector == "*"):
                        # if the results object doesn't already have this sector defined, we need to instantiate it
                        if searchSector not in result:
                           result[allSector] = {}
                           result[allSector]['tickers'] = []
                           result[allSector]['quotes'] = []
                        # stick it on
                        result[allSector]['tickers'] = self._storage[allSector].getTickers()
                        result[allSector]['quotes'] = self._storage[allSector].getQuoteList()

        #logging.info(result)
        return result

    # used for setting up _storage for searches by an individual company's stock's ticker as opposed to search by sector
    # reads MySQL contents and populates it into the _storage variable
    # the _storage variable is set up like this:
    # _storage[aStockTicker] which is a ticker object defined in services.py
    # then historical quotes are populated by calling .addQuote against each ticker object, which in turn
    # just adds them to the quote List in that object
    def tickerRead(self):
        # read from CSV
        self._storage: Dict[i.ticker] = {}
        sectors = {}

        # query the DB
        self._mycursor.execute('select w.quote_date, w.stock_code, w.open_price, w.high_price, w.low_price, w.close_price, w.volume, s.sector_code from weekly_stock_quotes w, stock s where s.stock_code=w.stock_code')

        # now get the weekly quotes for each stock
        for row in CursorByName(self._mycursor):
            if row['stock_code'] not in self._storage:
                self._storage[row['stock_code']] = i.ticker(tickerCode=row['stock_code'], sectorCode=row['sector_code'])
            
            self._storage[row['stock_code']].addQuote(row['quote_date'], row['open_price'], row['high_price'], row['low_price'], 0, row['close_price'], row['volume'])

        logging.info('Finished loading ticker:sector map. Total tickers is ' + str(len(self._storage)) + ' across ' + str(len(sectors)) + ' sectors with only stub quotes')

        # now populate the historical quotes
        # I don't have this data yet...
        # for later
        # self._storage[row['sectorticker']].addQuote(row['date'], row['open'], row['high'], row['low'], 0, row['close'], row['volume'])


    # the filtering happens in adapters but I don't know if I agree with this?  Shouldn't it be done in services?
    # 3. tickers - list of the tickers
    # 4. tickers/{ticker} - details of a specific ticker, including the sector it belongs to, and a list of dates we have quotes for it
    # ticker
    #  -sector
    #  -quote dates
    def get_tickers(self, filters: i.tickerFilter) -> List[i.ticker]:
        result = {}
        # loop through the tickers in our storage structure
        for allTicker in self._storage:
            # loop through the filters
            for searchTickerList in filters.tickers:
                if ( searchTickerList == allTicker ) or ( searchTickerList == "*" ):
                    result[allTicker] = {}
                    result[allTicker]['sector'] = self._storage[allTicker].getSector()
                    # call getQuoteList with a filter on it
                    result[allTicker]['quotes'] = self._storage[allTicker].getQuoteList()

                #for searchTicker in searchTickerList: 
                #    if ( searchTicker == allTicker ) or ( searchTicker == "*" ):
                #        result[allTicker] = {}
                #        result[allTicker]['sector'] = self._storage[allTicker].getSector()
                #        # call getQuoteList with a filter on it
                #        result[allTicker]['quotes'] = self._storage[allTicker].getQuoteList()
        #logging.info(result)
        
        return result