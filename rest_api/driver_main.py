from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from . import adapter_models, entity_schemas, usecase_rules
from .adapter_database import SessionLocal, engine
from sqlalchemy import tuple_

adapter_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# error handling
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"HTTP error in request: {repr(exc)}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"Invalid request data in: {exc}")
    return await request_validation_exception_handler(request, exc)


# request routing
@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


# USE CASE 1
# list stocks in database
# takes optional filter as a request query: 'stock_codes' which list of stock codes
@app.get("/stocks/", response_model=List[entity_schemas.Stock])
def show_records(filters: Optional[usecase_rules.stock_filter] = None, db: Session = Depends(get_db)):
    if filters == None:
        # catches no get query
        records = db.query(adapter_models.Stock).all()
        return records
    elif filters.stock_code == None:
        raise HTTPException(status_code=400, detail="Bad request. Acceptable Query parameter is 'stock_code'")
    else:
        records = db.query(adapter_models.Stock).filter(
            adapter_models.Stock.stock_code.in_(filters.stock_code)
        ).all()
        #records_dict = [u.__dict__ for u in records]
        return records


# USE CASE 2
# gets a specific stock code
# does not accept request queries 
@app.get("/stocks/{search_stock}", response_model=List[entity_schemas.Stock])
def show_records(search_stock: str, db: Session = Depends(get_db)):
    records = db.query(adapter_models.Stock).filter(
        adapter_models.Stock.stock_code==search_stock
    ).all()
    #records_dict = [u.__dict__ for u in records]
    return records


# USE CASE 3
# gets a list of the weekly quotes for a specific stock code {search_stock}
# needs to be modified to accept request query, which would be a list of dates
@app.get("/stocks/{search_stock}/quotes/weekly", response_model=List[entity_schemas.Weekly_Stock_Quotes])
def show_records(search_stock: str, filters: Optional[usecase_rules.date_filter] = None, db: Session = Depends(get_db)):
    if filters == None:
        # catches no get query
        records = db.query(adapter_models.Weekly_Stock_Quotes).filter(
            adapter_models.Weekly_Stock_Quotes.stock_code==search_stock
        ).all()
        #records_dict = [u.__dict__ for u in records]
        return records
    else:
        filters.processSearchDates()
        if filters.start == None or filters.end == None:
            # they sent something weird and the constructor wasn't able to translate it into something usable
            raise HTTPException(status_code=400, detail="Bad request. Acceptable Query parameters are 'start_date' and/or 'end_date', or 'period'")
        else:
            # they've set filters
            records = db.query(adapter_models.Weekly_Stock_Quotes).filter(
                adapter_models.Weekly_Stock_Quotes.stock_code==search_stock
            ).filter(
                adapter_models.Weekly_Stock_Quotes.quote_date >= filters.start,
                adapter_models.Weekly_Stock_Quotes.quote_date < filters.end,
            ).all()

            return records

# USE CASE 4
# gets a specific quote (specific stock, specific date)
# does not accept request queries
@app.get("/stocks/{search_stock}/quotes/weekly/{search_date}", response_model=List[entity_schemas.Weekly_Stock_Quotes])
def show_records(search_stock: str, search_date: str, db: Session = Depends(get_db)):
    
    records = db.query(adapter_models.Weekly_Stock_Quotes).\
        filter(adapter_models.Weekly_Stock_Quotes.stock_code==search_stock). \
        filter(adapter_models.Weekly_Stock_Quotes.quote_date==search_date)
    records_dict = [u.__dict__ for u in records]
    return records_dict
