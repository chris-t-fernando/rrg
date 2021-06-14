from typing import List
from baseTickerObject import baseTickerObject

class sectorQuote(baseTickerObject):
    _tickers: List

    # could just hand in a dict object...
    def __init__(self, ticker, quoteDate, priceOpen, priceHigh, priceLow, priceOffer, priceClose, volume):
        super().__init__(ticker, quoteDate, priceOpen, priceHigh, priceLow, priceOffer, priceClose, volume)
        self._tickers = []


    def getQuote(self):
        return {
            "ticker": self._ticker,
            "quoteDate": self._quoteDate,
            "priceOpen": self._priceOpen,
            "priceHigh": self._priceHigh,
            "priceLow": self._priceLow,
            "priceOffer": self._priceOffer,
            "priceClose": self._priceClose,
            "volume": self._volume
        }

    def getTickers(self):
        return self._tickers

    def addTicker(self, newTicker):
        self._tickers.append(newTicker)