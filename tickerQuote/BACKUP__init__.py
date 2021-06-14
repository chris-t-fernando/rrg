class tickerQuote:
    _ticker: str
    _quoteDate: str
    _priceOpen: float
    _priceHigh: float
    _priceClose: float
    _volume: float # maybe an int?
    _sector: str

    # could just hand in a dict object...
    def __init__(self, ticker, quoteDate, priceOpen, priceHigh, priceLow, priceOffer, priceClose, volume, sector):
        self._ticker = ticker
        self._quoteDate = quoteDate
        self._priceOpen = priceOpen
        self._priceHigh = priceHigh
        self._priceLow = priceLow
        self._priceOffer = priceOffer
        self._priceClose = priceClose
        self._volume = volume
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

    def getTicker(self):
        return self._ticker
    
    def getQuoteDate(self):
        return self._quoteDate
    
    def getPriceOpen(self):
        return self._priceOpen
    
    def getPriceHigh(self):
        return self._priceHigh
    
    def getPriceLow(self):
        return self._priceLow
    
    def getPriceOffer(self):
        return self._priceOffer

    def getPriceClose(self):
        return self._priceClose

    def getVolume(self):
        return self._volume

    def getSector(self):
        return self._sector