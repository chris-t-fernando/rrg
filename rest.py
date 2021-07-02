from typing import List, Dict
from fastapi import FastAPI, Depends, Body, Path
from pydantic import BaseModel
import services, adapters
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

app = FastAPI()

# REST API that offers ASX quotes as documents
# 0. root
# 1. sectors - list of the sectors
# 2. sectors/{sector} - details of that sector, including all of the tickers belonging to it, and a list of dates we have quotes for it
# 3. tickers - list of the tickers
# 4. tickers/{ticker} - details of a specific ticker, including the sector it belongs to, and a list of dates we have quotes for it
# 5. quotes - a list of the quote types we have (at the moment just weekly but could be daily etc)
# 6. quotes/weekly - a list of the organisation/search options - by ticker or by date
# 7. quotes/weekly/tickers/ - a list of the tickers we have weekly quotes for
# 8. quotes/weekly/tickers/{ticker} - the weekly quotes we have for this ticker
# 9. quotes/weekly/dates/ - a list of the dates we have quotes for that belong to this 
# 10. quotes/weekly/dates/{date} - a list of the the quotes we have for this date

# IMPLEMENTATION
# 0. root
@app.get("/")
async def root():
    return [
        '/sectors',
        '/tickers',
        '/quotes'
    ]


# 1. sectors - list of the sectors
def restGetSectors() -> services.useCaseGetSectors:
    storage = adapters.CSVStorage()
    storage.sectorRead()
    return services.useCaseGetSectors(storage)

@app.get('/sectors', response_model=Dict)
async def sectors(filters: services.sectorFilter, use_case=Depends(restGetSectors)):
    return use_case.getSectors(filters)


# 2. sectors/{sector} - details of that sector, including all of the tickers belonging to it, and a list of dates we have quotes for it
def restGetSectors() -> services.useCaseGetSectors:
    storage = adapters.CSVStorage()
    storage.sectorRead()
    return services.useCaseGetSectors(storage)

@app.get('/sectors/{sector}', response_model=Dict)
async def sectors(use_case=Depends(restGetSectors), sector: str = Path(..., title="Ticker to get")):
    # ignores any filters being handed in, because it would only filter tickers and the request has specified it anyway
    filter = services.sectorFilter(sectorTicker=[ sector ])
    return use_case.getSectors(filter)


# 3. tickers - list of the tickers
def restGetTickers() -> services.useCaseGetTickers:
    storage = adapters.CSVStorage()
    storage.tickerRead()
    return services.useCaseGetTickers(storage)

@app.get('/tickers', response_model=Dict)
async def sectors(filters: services.tickerFilter, use_case=Depends(restGetTickers)):
    return use_case.getTickers(filters)


# 4. tickers/{ticker} - details of a specific ticker, including the sector it belongs to, and a list of dates we have quotes for it
def restGetTickers() -> services.useCaseGetTickers:
    storage = adapters.CSVStorage()
    storage.tickerRead()
    return services.useCaseGetTickers(storage)

@app.get('/tickers/{ticker}', response_model=Dict)
async def sectors(use_case=Depends(restGetTickers), ticker: str = Path(..., title="Ticker to get")):
    # ignores any filters being handed in, because it would only filter tickers and the request has specified it anyway
    filter = services.tickerFilter(tickers=[ ticker ])
    return use_case.getTickers(filter)


# 5. quotes - a list of the quote types we have (at the moment just weekly but could be daily etc)
# STUB
# todo: care more and programmatically work it out
@app.get('/quotes', response_model=List)
async def sectors():
    results = [ 'weekly' ]
    return results


# 6. tickers/{ticker} - details of a specific ticker, including the sector it belongs to, and a list of dates we have quotes for it
# STUB
# todo: care more and programmatically work it out
# todo: replace weekly with {interval}
@app.get('/quotes/weekly', response_model=List)
async def sectors():
    results = [ 'tickers', 'dates' ]
    return results


# 7. quotes/weekly/tickers/ - a list of the tickers we have weekly quotes for
# todo: replace weekly with {interval}
def restGetTickers() -> services.useCaseGetTickers:
    storage = adapters.CSVStorage()
    storage.tickerRead()
    return services.useCaseGetTickers(storage)

@app.get('/quotes/weekly/tickers', response_model=Dict)
async def sectors(filters: services.tickerFilter, use_case=Depends(restGetTickers)):
    # override/set quote type filter to weekly, since this is the rest document called
    filters.setQuoteTypeFilter('weekly')
    return use_case.getTickers(filters)


# 8. quotes/weekly/tickers/{ticker} - the weekly quotes we have for this ticker
# todo: replace weekly with {interval}
def restGetTickers() -> services.useCaseGetTickers:
    storage = adapters.CSVStorage()
    storage.tickerRead()
    return services.useCaseGetTickers(storage)

@app.get('/quotes/weekly/tickers/{ticker}', response_model=Dict)
async def sectors(use_case=Depends(restGetTickers), ticker: str = Path(..., title="Ticker to get")):
    # ignores any filters being handed in, because it would only filter tickers and the request has specified it anyway
    filter = services.tickerFilter(tickers=[ ticker ])
    filter.setQuoteTypeFilter('weekly')
    return use_case.getTickers(filter)


# 9. quotes/weekly/dates/ - a list of the dates we have quotes for that belong to this
# todo: replace weekly with {interval}
def restGetTickers() -> services.useCaseGetTickers:
    storage = adapters.CSVStorage()
    storage.tickerRead()
    return services.useCaseGetTickers(storage)

@app.get('/quotes/weekly/tickers', response_model=Dict)
async def sectors(filters: services.tickerFilter, use_case=Depends(restGetTickers)):
    # override/set quote type filter to weekly, since this is the rest document called
    filters.setQuoteTypeFilter('weekly')
    return use_case.getTickers(filters)
