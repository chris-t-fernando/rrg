from baseTickerObject import baseTickerObject

class tickerQuote(baseTickerObject):
    _sector: str

    # could just hand in a dict object...
    def __init__(self, ticker, quoteDate, priceOpen, priceHigh, priceLow, priceOffer, priceClose, volume, sector):
        super().__init__(ticker, quoteDate, priceOpen, priceHigh, priceLow, priceOffer, priceClose, volume)
        self._sector = sector
    
    def getQuote(self):
        return {
            "ticker": self._ticker,
            "quoteDate": self._quoteDate,
            "priceOpen": self._priceOpen,
            "priceHigh": self._priceHigh,
            "priceLow": self._priceLow,
            "priceOffer": self._priceOffer,
            "priceClose": self._priceClose,
            "volume": self._volume,
            "sector": self._sector
        }

    def getSector(self):
        return self._sector