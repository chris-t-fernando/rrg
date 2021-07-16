from typing import List, Optional
from datetime import date
from fastapi import Depends, FastAPI, HTTPException, Query, Body, Response, status
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


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")


# STOCK QUOTE LITERAL RETURNS
@app.get("/quote", response_model=List[str])
def main():
    return ["stock", "sector"]


@app.get("/quote/stock", response_model=List[str])
def main():
    return ["intraday", "daily", "weekly"]


@app.get("/quote/stock/intraday", response_model=str)
def main():
    return "Not implemented"


@app.get("/quote/stock/daily", response_model=List[str])
def main():
    return "Not implemented"


#  QUOTE LITERAL RETURNS
@app.get("/quote/sector", response_model=List[str])
def main():
    return ["intraday", "daily", "weekly"]


@app.get("/quote/sector/intraday", response_model=str)
def main():
    return "Not implemented"


@app.get("/quote/sector/daily", response_model=List[str])
def main():
    return "Not implemented"


# STOCK USE CASE 1
# list stocks in database
# takes optional filter as a request query: 'stock_codes' which list of stock codes
@app.get("/stock/", response_model=List[entity_schemas.Stock])
def show_records(
    filters: Optional[usecase_rules.stock_filter] = None,
    db: Session = Depends(get_db),
):
    if filters == None or filters.stock_code == None:
        # catches no get query
        return db.query(adapter_models.Stock).all()

    else:
        # validate the queried stocks
        return (
            db.query(adapter_models.Stock)
            .filter(adapter_models.Stock.stock_code.in_(filters.stock_code))
            .all()
        )


# STOCK USE CASE 2
# gets a specific stock code
# does not accept request queries
@app.get(
    "/stock/{search_stock}",
    response_model=List[entity_schemas.Stock],
    status_code=status.HTTP_200_OK,
)
def show_records(response: Response, search_stock: str, db: Session = Depends(get_db)):
    records = (
        db.query(adapter_models.Stock)
        .filter(adapter_models.Stock.stock_code == search_stock)
        .all()
    )
    if len(records) > 0:
        return records
    else:
        raise HTTPException(
            status_code=404,
            detail="No results found",
        )


# STOCK USE CASE 3
# gets a list of the weekly quotes for a specific stock code {search_stock}
@app.get(
    "/stock/{search_stock}/quotes/weekly",
    response_model=List[entity_schemas.Weekly_Stock_Quotes],
)
def show_records(
    search_stock: str,
    filters: Optional[usecase_rules.date_filter] = None,
    db: Session = Depends(get_db),
):
    if filters == None:
        # catches no get query
        results = (
            db.query(adapter_models.Weekly_Stock_Quotes)
            .filter(adapter_models.Weekly_Stock_Quotes.stock_code == search_stock)
            .all()
        )
        if len(results) > 0:
            return results
        else:
            raise HTTPException(
                status_code=404,
                detail="No results found",
            )
    else:
        processSearchDates = filters.processSearchDates()
        if processSearchDates == False:
            raise HTTPException(
                status_code=400,
                detail="Bad request",
            )
        if filters.start == None or filters.end == None:
            # they sent something weird and the constructor wasn't able to translate it into something usable
            raise HTTPException(
                status_code=400,
                detail="Bad request. Acceptable Query parameters are 'start_date' and/or 'end_date', or 'period'",
            )
        else:
            # they've set filters
            results = (
                db.query(adapter_models.Weekly_Stock_Quotes)
                .filter(adapter_models.Weekly_Stock_Quotes.stock_code == search_stock)
                .filter(
                    adapter_models.Weekly_Stock_Quotes.quote_date >= filters.start,
                    adapter_models.Weekly_Stock_Quotes.quote_date < filters.end,
                )
                .all()
            )
            if len(results) > 0:
                return results
            else:
                raise HTTPException(
                    status_code=404,
                    detail="No results not found",
                )


# STOCK USE CASE 4
# gets a specific quote (specific stock, specific date)
# does not accept request queries
@app.get(
    "/stock/{search_stock}/quotes/weekly/{search_date}",
    response_model=List[entity_schemas.Weekly_Stock_Quotes],
)
def show_records(search_stock: str, search_date: str, db: Session = Depends(get_db)):

    results = (
        db.query(adapter_models.Weekly_Stock_Quotes)
        .filter(adapter_models.Weekly_Stock_Quotes.stock_code == search_stock)
        .filter(adapter_models.Weekly_Stock_Quotes.quote_date == search_date)
        .all()
    )
    if len(results) > 0:
        return results

    else:
        raise HTTPException(
            status_code=404,
            detail="No results not found",
        )


# some template code for later - if i want to check individual stock codes exist
# i don't care right now
#        # all of the stocks we know about
#        queryStockCollection = usecase_rules.stock_collection(records)
#
#        # check if there are stocks being queried that we don't know about
#        diff = queryStockCollection.diffCollection(filters.stock_code)
#        if len(diff) == 0:
#            # found all of them
#            return records
#        else:
#            response.status_code = status.HTTP_207_MULTI_STATUS


# STOCK USE CASE 5
# gets all of the dates we have weekly quotes for
# takes optional filter as a request query: 'stock_codes' which list of stock codes
@app.get("/quote/stock/weekly", response_model=List)
def show_records(
    filters: Optional[usecase_rules.stock_filter] = None, db: Session = Depends(get_db)
):
    if filters == None:
        # catches no get query
        # can't just return .distinct.all() because that would be a dict with quote_date as key and the date as val
        # whereas what we really want here is a flat list of dates
        returnList = []
        records = (
            db.query(adapter_models.Weekly_Stock_Quotes.quote_date).distinct().all()
        )
        [returnList.append(u.quote_date) for u in records]
        return returnList
    elif filters.stock_code == None:
        raise HTTPException(
            status_code=400,
            detail="Bad request. Acceptable Query parameter is 'stock_code'",
        )
    else:
        returnList = []
        records = (
            db.query(adapter_models.Weekly_Stock_Quotes.quote_date)
            .filter(
                adapter_models.Weekly_Stock_Quotes.stock_code.in_(filters.stock_code)
            )
            .distinct()
            .all()
        )
        [returnList.append(u.quote_date) for u in records]
        return returnList


# STOCK USE CASE 6
# gets the quotes for all (or filtered list of) stock codes
# takes optional filter as a request query: 'stock_codes' which list of stock codes
# todo: accept sector as a filter
@app.get(
    "/quote/stock/weekly/{search_date}",
    response_model=List[entity_schemas.Weekly_Stock_Quotes],
)
def show_records(
    search_date: str,
    db: Session = Depends(get_db),
    filters: Optional[usecase_rules.stock_filter] = None,
):
    if filters == None:
        results = (
            db.query(adapter_models.Weekly_Stock_Quotes)
            .filter(adapter_models.Weekly_Stock_Quotes.quote_date == search_date)
            .all()
        )
        if len(results) > 0:
            return results
        else:
            raise HTTPException(
                status_code=404,
                detail="No results found",
            )
    elif filters.stock_code == None:
        raise HTTPException(
            status_code=400,
            detail="Bad request. Acceptable Query parameter is 'stock_code'",
        )
    else:
        results = (
            db.query(adapter_models.Weekly_Stock_Quotes)
            .filter(adapter_models.Weekly_Stock_Quotes.quote_date == search_date)
            .filter(
                adapter_models.Weekly_Stock_Quotes.stock_code.in_(filters.stock_code)
            )
            .all()
        )
        if len(results) > 0:
            return results
        else:
            raise HTTPException(
                status_code=404,
                detail="No results found",
            )


#######################
###### SECTOR #########
#######################

# SECTOR USE CASE 1
# list sectors in database
# takes optional filter as a request query: 'sector_codes' which list of sector codes
@app.get("/sector/", response_model=List[entity_schemas.Sector])
def show_records(
    filters: Optional[usecase_rules.sector_filter] = None,
    db: Session = Depends(get_db),
):
    if filters == None or filters.sector_code == None:
        # catches no get query
        return db.query(adapter_models.Sector).all()

    else:
        # validate the queried sectors
        return (
            db.query(adapter_models.Sector)
            .filter(adapter_models.Sector.sector_code.in_(filters.sector_code))
            .all()
        )


# SECTOR USE CASE 2
# gets a specific sector code
# does not accept request queries
@app.get(
    "/sector/{search_sector}",
    response_model=List[entity_schemas.Sector],
    status_code=status.HTTP_200_OK,
)
def show_records(response: Response, search_sector: str, db: Session = Depends(get_db)):
    records = (
        db.query(adapter_models.Sector)
        .filter(adapter_models.Sector.sector_code == search_sector)
        .all()
    )
    if len(records) > 0:
        return records
    else:
        raise HTTPException(
            status_code=404,
            detail="No results found",
        )


# SECTOR USE CASE 3
# gets a list of the weekly quotes for a specific sector code {search_sector}
@app.get(
    "/sector/{search_sector}/quotes/weekly",
    response_model=List[entity_schemas.Weekly_Sector_Quotes],
)
def show_records(
    search_sector: str,
    filters: Optional[usecase_rules.date_filter] = None,
    db: Session = Depends(get_db),
):
    if filters == None:
        # catches no get query
        results = (
            db.query(adapter_models.Weekly_Sector_Quotes)
            .filter(adapter_models.Weekly_Sector_Quotes.sector_code == search_sector)
            .all()
        )
        if len(results) > 0:
            return results
        else:
            raise HTTPException(
                status_code=404,
                detail="No results found",
            )
    else:
        processSearchDates = filters.processSearchDates()
        if processSearchDates == False:
            raise HTTPException(
                status_code=400,
                detail="Bad request",
            )
        if filters.start == None or filters.end == None:
            # they sent something weird and the constructor wasn't able to translate it into something usable
            raise HTTPException(
                status_code=400,
                detail="Bad request. Acceptable Query parameters are 'start_date' and/or 'end_date', or 'period'",
            )
        else:
            # they've set filters
            results = (
                db.query(adapter_models.Weekly_Sector_Quotes)
                .filter(
                    adapter_models.Weekly_Sector_Quotes.sector_code == search_sector
                )
                .filter(
                    adapter_models.Weekly_Sector_Quotes.quote_date >= filters.start,
                    adapter_models.Weekly_Sector_Quotes.quote_date < filters.end,
                )
                .all()
            )
            if len(results) > 0:
                return results
            else:
                raise HTTPException(
                    status_code=404,
                    detail="No results not found",
                )


# SECTOR USE CASE 4
# gets a specific quote (specific sector, specific date)
# does not accept request queries
@app.get(
    "/sector/{search_sector}/quotes/weekly/{search_date}",
    response_model=List[entity_schemas.Weekly_Sector_Quotes],
)
def show_records(search_sector: str, search_date: str, db: Session = Depends(get_db)):

    results = (
        db.query(adapter_models.Weekly_Sector_Quotes)
        .filter(adapter_models.Weekly_Sector_Quotes.sector_code == search_sector)
        .filter(adapter_models.Weekly_Sector_Quotes.quote_date == search_date)
        .all()
    )
    if len(results) > 0:
        return results

    else:
        raise HTTPException(
            status_code=404,
            detail="No results not found",
        )


# some template code for later - if i want to check individual sector codes exist
# i don't care right now
#        # all of the sectors we know about
#        querySectorCollection = usecase_rules.sector_collection(records)
#
#        # check if there are sectors being queried that we don't know about
#        diff = querySectorCollection.diffCollection(filters.sector_code)
#        if len(diff) == 0:
#            # found all of them
#            return records
#        else:
#            response.status_code = status.HTTP_207_MULTI_STATUS


# SECTOR USE CASE 5
# gets all of the dates we have weekly quotes for
# takes optional filter as a request query: 'sector_codes' which list of sector codes
@app.get("/quote/sector/weekly", response_model=List)
def show_records(
    filters: Optional[usecase_rules.sector_filter] = None, db: Session = Depends(get_db)
):
    if filters == None:
        # catches no get query
        # can't just return .distinct.all() because that would be a dict with quote_date as key and the date as val
        # whereas what we really want here is a flat list of dates
        returnList = []
        records = (
            db.query(adapter_models.Weekly_Sector_Quotes.quote_date).distinct().all()
        )
        [returnList.append(u.quote_date) for u in records]
        return returnList
    elif filters.sector_code == None:
        raise HTTPException(
            status_code=400,
            detail="Bad request. Acceptable Query parameter is 'sector_code'",
        )
    else:
        returnList = []
        records = (
            db.query(adapter_models.Weekly_Sector_Quotes.quote_date)
            .filter(
                adapter_models.Weekly_Sector_Quotes.sector_code.in_(filters.sector_code)
            )
            .distinct()
            .all()
        )
        [returnList.append(u.quote_date) for u in records]
        return returnList


# SECTOR USE CASE 6
# gets the quotes for all (or filtered list of) sector codes
# takes optional filter as a request query: 'sector_codes' which list of sector codes
# todo: accept sector as a filter
@app.get(
    "/quote/sector/weekly/{search_date}",
    response_model=List[entity_schemas.Weekly_Sector_Quotes],
)
def show_records(
    search_date: str,
    db: Session = Depends(get_db),
    filters: Optional[usecase_rules.sector_filter] = None,
):
    if filters == None:
        results = (
            db.query(adapter_models.Weekly_Sector_Quotes)
            .filter(adapter_models.Weekly_Sector_Quotes.quote_date == search_date)
            .all()
        )
        if len(results) > 0:
            return results
        else:
            raise HTTPException(
                status_code=404,
                detail="No results found",
            )
    elif filters.sector_code == None:
        raise HTTPException(
            status_code=400,
            detail="Bad request. Acceptable Query parameter is 'sector_code'",
        )
    else:
        results = (
            db.query(adapter_models.Weekly_Sector_Quotes)
            .filter(adapter_models.Weekly_Sector_Quotes.quote_date == search_date)
            .filter(
                adapter_models.Weekly_Sector_Quotes.sector_code.in_(filters.sector_code)
            )
            .all()
        )
        if len(results) > 0:
            return results
        else:
            raise HTTPException(
                status_code=404,
                detail="No results found",
            )
