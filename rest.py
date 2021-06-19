from typing import List, Dict
from fastapi import FastAPI, Depends, Body, Path
from pydantic import BaseModel
import services, adapters
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

app = FastAPI()

# REST API that offers a ASX documents
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

# implementation
# 1. sectors - list of the sectors
def restGetSectors() -> services.useCaseGetSectors:
    storage = adapters.CSVStorage()
    storage.sectorRead()
    return services.useCaseGetSectors(storage)

@app.post('/sectors', response_model=Dict)
async def sectors(filters: services.sectorFilter, use_case=Depends(restGetSectors)):
    return use_case.getSectors(filters)


# 2. sectors/{sector} - details of that sector, including all of the tickers belonging to it, and a list of dates we have quotes for it
def restGetSectors() -> services.useCaseGetSectors:
    storage = adapters.CSVStorage()
    storage.sectorRead()
    return services.useCaseGetSectors(storage)

@app.post('/sectors/{sector}', response_model=Dict)
async def sectors(use_case=Depends(restGetSectors), sector: str = Path(..., title="Ticker to get")):
    # ignores any filters being handed in, because it would only filter tickers and the request has specified it anyway
    filter = services.sectorFilter(sectorTicker=[ sector ])
    return use_case.getSectors(filter)

# 3. tickers - list of the tickers
def restGetTickers() -> services.useCaseGetTickers:
    storage = adapters.CSVStorage()
    storage.tickerRead()
    return services.useCaseGetTickers(storage)

@app.post('/tickers', response_model=Dict)
async def sectors(filters: services.tickerFilter, use_case=Depends(restGetTickers)):
    return use_case.getTickers(filters)

# 4. tickers/{ticker} - details of a specific ticker, including the sector it belongs to, and a list of dates we have quotes for it
def restGetTickers() -> services.useCaseGetTickers:
    storage = adapters.CSVStorage()
    storage.tickerRead()
    return services.useCaseGetTickers(storage)

@app.post('/tickers/{ticker}', response_model=Dict)
async def sectors(use_case=Depends(restGetTickers), ticker: str = Path(..., title="Ticker to get")):
    # ignores any filters being handed in, because it would only filter tickers and the request has specified it anyway
    filter = services.tickerFilter(tickers=[ ticker ])
    return use_case.getTickers(filter)

# 5. quotes - a list of the quote types we have (at the moment just weekly but could be daily etc)
# STUB
@app.post('/quotes', response_model=List)
async def sectors():
    results = [ 'weekly' ]
    return results
