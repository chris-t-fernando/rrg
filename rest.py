from typing import List
from fastapi import FastAPI, Depends, Body
from pydantic import BaseModel
import services, adapters
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

app = FastAPI()

def restGetSectors() -> services.useCaseGetSectors:
    return services.useCaseGetSectors(adapters.CSVStorage())

@app.post('/sectors', response_model=List[services.sectorTicker])
async def sectors(filters: services.sectorFilter, use_case=Depends(restGetSectors)):
    return use_case.getSectors(filters)

"""
-offers functions called getSectors, getAllTickersInSector, getTickersSector, getSectorQuotesBetweenDates, getSectorQuotesOnDate
--hands these an adapters.RDS()
-it also has a series of functions for each of the use cases above

back to rest
-i guess each function then has the opportunity to do what it needs
--translate to JSON, or send it to eventbridge

"""

"""
def get_use_case() -> services.RoomListUseCase:
    return services.RoomListUseCase(adapters.MemoryStorage())


@app.post("/rooms", response_model=List[services.Room])
def rooms(filters: services.RoomFilter, use_case=Depends(get_use_case)):
    return use_case.show_rooms(filters)
"""

