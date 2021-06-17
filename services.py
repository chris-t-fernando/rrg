from typing import Optional, List
from pydantic import BaseModel
import logging, sys
from sectorQuote import sectorQuote
from pprint import pprint
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

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

class sectorFilter(BaseModel):
    sectorTicker: List
    
class sectorStorage:
    def get_sectors(self, filters: sectorFilter) -> List[sectorTicker]: ...

class useCaseGetSectors():
    def __init__(self, source: sectorStorage):
        self.source = source
    
    def getSectors(self, filters: sectorFilter) -> List[sectorTicker]:
        sectors = self.source.get_sectors(filters=filters)
        return sectors