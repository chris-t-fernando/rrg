from typing import Optional, List
from pydantic import BaseModel
import logging, sys
from sectorQuote import sectorQuote
from tickerQuote import tickerQuote
from pprint import pprint
logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# todo: this is a duplication of sectorQuote - I should merge the two to collapse/simplify
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

# todo: this is a duplication of tickerQuote - I should merge the two to collapse/simplify
class ticker(BaseModel):
    tickerCode: str
    sectorCode: str
    quotes: dict
    
    quotes = {}

    def addQuote(self, date, open, high, low, offer, close, volume):
        self.quotes[date] = tickerQuote(self.tickerCode, date, open, high, low, offer, close, volume, self.sectorCode)
    
    def getQuoteList(self):
        returnDates = []
        for date in self.quotes:
            returnDates.append(date)
        return returnDates
    
    def getSector(self):
        return self.sectorCode


class sectorFilter(BaseModel):
    sectorTicker: List

class tickerFilter(BaseModel):
    tickers: List
    quoteType: Optional[List] = None

    def setQuoteTypeFilter(self, newQuoteList):
        self.quoteType = newQuoteList
    
    def setQuoteTickerFilter(self, newTickerFilter):
        self.tickers = newTickerFilter

class sectorStorage:
    def get_sectors(self, filters: sectorFilter) -> List[sectorTicker]: ...

class tickerStorage:
    def get_tickers(self, filters: tickerFilter) -> List[ticker]: ...

class tickerWeeklyStorage:
    def get_weekly_tickers(self, filters: tickerFilter) -> List[ticker]: ...

# gets sectors from storage
class useCaseGetSectors():
    def __init__(self, source: sectorStorage):
        self.source = source
    
    def getSectors(self, filters: sectorFilter) -> List[sectorTicker]:
        return self.source.get_sectors(filters=filters)

# gets individual company tickers from storage
class useCaseGetTickers():
    def __init__(self, source: tickerStorage):
        self.source = source
    
    def getTickers(self, filters: tickerFilter) -> List[ticker]:
        return self.source.get_tickers(filters=filters)

    def getWeeklyTickers(self, filters: tickerFilter) -> List[ticker]:
        return self.source.get_weekly_tickers(filters=filters)
