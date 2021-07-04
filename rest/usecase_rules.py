from typing import Optional, List
from pydantic import BaseModel

class stock_filter(BaseModel):
    stock_code: Optional[List] = None