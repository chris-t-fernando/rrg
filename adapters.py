from typing import List, Dict
import services as i
import logging, sys
import csv
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# need to rewrite this so that the rest api calls a storage object, which in turn calls another object that does the 
# reading from json or csv or whatever, and then this object below just loads that data into the services objectsffr44ryedwasy6trfvgghhbjnabbc12222354567890`1234567890
class CSVStorage(i.sectorStorage):
    def __init__(self):
        # read from CSV

        self._storage: Dict[i.sectorTicker] = {}
        tickerCount = 0

        # populate sectors, which is a Dict (key sector ticker) containing
        # ['tickers'], which is a List of tickers belonging to this sector
        # ['quotes'], which is a Dict of historical quotes for this ticker
        # start with creating the object and populating ['tickers']
        with open('sector-ticker-map.csv', newline='') as csvfile:
            mapReader = csv.DictReader(csvfile, delimiter=',')

            for row in mapReader:
                # if the sector key doesn't exist, create it
                sector = row['sector'].lower()
                if sector not in self._storage:
                    self._storage[sector] = i.sectorTicker(sectorTickerCode=sector)
                
                ticker = row['ticker'].lower()

                self._storage[sector].addTicker(ticker)
                tickerCount += 1

        logging.debug('Finished loading sector:ticker map. Total sectors is ' +  str(len(self._storage)) + ', total tickers is ' + str(tickerCount))

        # now populate the historical quotes
        with open('sectors.csv', newline='') as csvfile:
            tickerReader = csv.DictReader(csvfile, delimiter=',')
            quoteCount = 0
            for row in tickerReader:
                # todo - I forgot to add 'offer'.  I don't think I'll use it but noting just in case.  hardcoding to 0 because I'm lazy
                self._storage[row['sectorticker']].addQuote(row['date'], row['open'], row['high'], row['low'], 0, row['close'], row['volume'])
                quoteCount += 1
        
        logging.debug('Finished loading ' + str(quoteCount) + ' sector quotes')


    # the filtering happens in adapters but I don't know if I agree with this?  Shouldn't it be done in services?
    # 2. sectors/{sector} - details of that sector, including all of the tickers belonging to it, and a list of dates we have quotes for it
    # sector
    #  -tickers
    #  -quote dates
    def get_sectors(self, filters: i.sectorFilter) -> List[i.sectorTicker]:
        result = {}

        for allSector in self._storage:
            for searchSectorList in filters:
                for searchSector in searchSectorList[1]:
                   if ( searchSector == allSector ) or ( searchSector == "*"):
                        if searchSector not in result:
                           result[allSector] = {}
                           result[allSector]['tickers'] = []
                           result[allSector]['quotes'] = []
                        result[allSector]['tickers'] = self._storage[allSector].getTickers()
                        result[allSector]['quotes'] = self._storage[allSector].getQuoteList()

        #logging.debug(result)
        return result

