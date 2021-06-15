from typing import Optional, List
from pydantic import BaseModel
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class sectorList:
    someVar = 'something'

class sectorTicker(BaseModel):
    something: int
    something = 2

class sectorFilter(BaseModel):
    sectorTicker: int
    
class sectorStorage:
    def get_sectors(self, filters: sectorFilter) -> List[sectorTicker]: ...

class useCaseGetSectors():
    def __init__(self, source: sectorStorage):
        self.source = source
    
    def getSectors(self, filters: sectorFilter) -> List[sectorTicker]:
        sectors = self.source.get_sectors(filters=filters)
        return sectors