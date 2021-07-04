from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
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


@app.get("/")
def main():
    return RedirectResponse(url="/docs/")



@app.get("/stocks/", response_model=List[entity_schemas.Stock])
def show_records(filters: Optional[usecase_rules.stock_filter] = None, db: Session = Depends(get_db)):
    if filters == None:
        records = db.query(adapter_models.Stock).all()
        return records
    else:
        records = db.query(adapter_models.Stock).filter(
            adapter_models.Stock.stock_code.in_(filters.stock_code)
        )
        records_dict = [u.__dict__ for u in records]
        return records_dict


@app.get("/stocks/{search_stock}", response_model=List[entity_schemas.Stock])
def show_records(search_stock: str, db: Session = Depends(get_db)):
    records = db.query(adapter_models.Stock).filter(adapter_models.Stock.stock_code==search_stock)
    records_dict = [u.__dict__ for u in records]
    return records_dict


@app.get("/stocks/{search_stock}/quotes/weekly", response_model=List[entity_schemas.Weekly_Stock_Quotes])
def show_records(search_stock: str, db: Session = Depends(get_db)):
    
    records = db.query(adapter_models.Weekly_Stock_Quotes).filter(adapter_models.Weekly_Stock_Quotes.stock_code==search_stock)
    records_dict = [u.__dict__ for u in records]
    return records_dict


@app.get("/stocks/{search_stock}/quotes/weekly/{search_date}", response_model=List[entity_schemas.Weekly_Stock_Quotes])
def show_records(search_stock: str, search_date: str, db: Session = Depends(get_db)):
    
    records = db.query(adapter_models.Weekly_Stock_Quotes).\
        filter(adapter_models.Weekly_Stock_Quotes.stock_code==search_stock). \
        filter(adapter_models.Weekly_Stock_Quotes.quote_date==search_date)
    records_dict = [u.__dict__ for u in records]
    return records_dict
