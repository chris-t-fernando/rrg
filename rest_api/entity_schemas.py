from datetime import date
from pydantic import BaseModel


class Stock(BaseModel):
    stock_code: str
    stock_name: str
    sector_code: str

    class Config:
        orm_mode = True

class Sector(BaseModel):
    sector_code: str
    sector_name: str

    class Config:
        orm_mode = True

class Weekly_Stock_Quotes(BaseModel):
    quote_date: date
    stock_code: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int

    class Config:
        orm_mode = True

class Weekly_Sector_Quotes(BaseModel):
    quote_date: date
    sector_code: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int

    class Config:
        orm_mode = True

#class Weekly_Stock_Quotes_List(BaseModel):
#    quote_date: date
#    
#    class Config:
#        orm_mode = True
