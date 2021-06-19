from typing import Optional, List
from pydantic import BaseModel
import logging, sys
from sectorQuote import sectorQuote
from tickerQuote import tickerQuote
from pprint import pprint
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

# this is a duplication of sectorQuote - not sure which one I want to use right now though
class sectorTicker(BaseModel):
    sectorTickerCode: str
    quotes: dict
    tickers: list
    
    quotes = {}
    tickers = []

    def addTicker(self, theTicker: str):
        self.tickers.append(theTicker)

    def addQuote(self, date, open, high, low, offer, close, volume):
        self.quotes[date] = sectorQuote(self.sectorTickerCode, date, open, high, low, offer, close, volume)

    def getTickers(self):
        return self.tickers
    
    def getQuoteList(self):
        returnDates = []
        for date in self.quotes:
            returnDates.append(date)
        return returnDates

# this is a duplication of tickerQuote - not sure which one I want to use right now though
class ticker(BaseModel):
    sectorTickerCode: str
    quotes: dict
    
    quotes = {}

    def addQuote(self, date, open, high, low, offer, close, volume):
        self.quotes[date] = tickerQuote(self.sectorTickerCode, date, open, high, low, offer, close, volume)
    
    def getQuoteList(self):
        returnDates = []
        for date in self.quotes:
            returnDates.append(date)
        return returnDates


class sectorFilter(BaseModel):
    sectorTicker: List

class tickerFilter(BaseModel):
    tickers: List

class sectorStorage:
    def get_sectors(self, filters: sectorFilter) -> List[sectorTicker]: ...

class tickerStorage:
    def get_tickers(self, filters: tickerFilter) -> List[ticker]: ...


class useCaseGetSectors():
    def __init__(self, source: sectorStorage):
        self.source = source
    
    def getSectors(self, filters: sectorFilter) -> List[sectorTicker]:
        #sectors = self.source.get_sectors(filters=filters)
        #return sectors
        return self.source.get_sectors(filters=filters)

class useCaseGetTickers():
    def __init__(self, source: tickerStorage):
        self.source = source
    
    def getTickers(self, filters: tickerFilter) -> List[ticker]:
        #sectors = self.source.get_tickers(filters=filters)
        #return sectors
        return self.source.get_tickers(filters=filters)