from typing import List
import services as i
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class CSVStorage(i.sectorStorage):
    def __init__(self):
        # read from CSV
        self._storage: List[i.sectorTicker] = [
            i.sectorTicker()
        ]

    def get_sectors(self, filters: i.sectorFilter) -> List[i.sectorTicker]:
        result = self._storage
        return result