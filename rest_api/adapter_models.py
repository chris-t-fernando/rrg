from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.types import Date
from .adapter_database import Base


class Stock(Base):
    __tablename__ = "stock"

    stock_code = Column(String(6), primary_key=True, index=True)
    stock_name = Column(String(255))
    sector_code = Column(String(3))

class Sector(Base):
    __tablename__ = "sector"

    sector_code = Column(String(3), primary_key=True, index=True)
    sector_name = Column(String(255))

class Weekly_Stock_Quotes(Base):
    __tablename__ = "weekly_stock_quotes"

    quote_date = Column(Date(), primary_key=True, index=True)
    stock_code = Column(String(6), primary_key=True, index=True)
    open_price = Column(Float())
    high_price = Column(Float())
    low_price = Column(Float())
    close_price = Column(Float())
    volume = Column(Integer())

class Weekly_Sector_Quotes(Base):
    __tablename__ = "weekly_sector_quotes"

    quote_date = Column(Date(), primary_key=True, index=True)
    sector_code = Column(String(3), primary_key=True, index=True)
    open_price = Column(Float())
    high_price = Column(Float())
    low_price = Column(Float())
    close_price = Column(Float())
    volume = Column(Integer())