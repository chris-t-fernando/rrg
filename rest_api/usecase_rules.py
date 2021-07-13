from sys import float_repr_style
from typing import Optional, List, Dict
from pydantic import BaseModel, ValidationError, root_validator, validator
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class stock(BaseModel):
    stock_code: str
    stock_name: str
    sector_code: str

    @root_validator()
    def check_stock(cls, values):
        assert (
            len(values.get("stock_code")) >= 3 and len(values.get("stock_code")) <= 5
        ), "stock_code must be between 3 and 5 characters long"
        assert (
            len(values.get("stock_name")) <= 30
        ), "stock_name must be less than 30 characters long"
        assert (
            len(values.get("sector_code")) == 3
        ), "sector_code must be exactly 3 characters long"
        return values


class stock_collection:
    stockCollection = []

    def __init__(self, stocks: List):
        # make sure there aren't any duplicate stock codes passed in
        if self.checkUnique(stocks):
            [
                self.stockCollection.append(
                    stock(
                        stock_code=x.stock_code,
                        stock_name=x.stock_name,
                        sector_code=x.sector_code,
                    )
                )
                for x in stocks
            ]
        else:
            return False

    def diffCollection(self, queryStocks: List):
        # make sure there aren't any duplicate stocks being queried
        assert self.checkUnique(queryStocks), (
            "Duplicate stock_codes in list: [ "
            + ", ".join([str(elem) for elem in queryStocks])
            + " ]"
        )
        notInCollection = []

        if all(elem in self.stockCollection for elem in queryStocks):
            return []
        else:
            notFound = []
            for qStock in queryStocks:
                found = False
                for cStock in self.stockCollection:
                    if qStock == cStock.stock_code:
                        found = True
                        break
                if not found:
                    notFound.append(qStock)
            return notFound

    def checkUnique(self, someList: List):
        return len(someList) == len(set(someList))

    def getDuplicates(self, someList: List):
        seen = set()
        uniq = [x for x in someList if x in seen or seen.add(x)]
        return seen


class stock_filter(BaseModel):
    stock_code: Optional[List] = None

    @root_validator()
    def check_stock_filter(cls, values: Dict[str, List[str]]) -> Dict[str, List[str]]:
        # optional, so none is okay
        if values.get("stock_code") == None:
            # but just make sure there's no other attributes set
            assert len(values) == 0, "invalid attribute: " + str(values.keys())
            return values

        assert len(values) == 1, "multiple attributes given, expecting just stock_code"
        assert "stock_code" in values, "unknown attribute given in " + str(
            values.keys()
        )
        for x in values.get("stock_code"):
            assert len(x) >= 2 and len(x) <= 6, (
                "stock_codes must be between 3 and 5 characters long.  Failed on '"
                + x
                + "'"
            )

        return values


class sector_filter(BaseModel):
    sector_code: Optional[List] = None

    @root_validator()
    def check_sector_filter(cls, values: Dict[str, List[str]]) -> Dict[str, List[str]]:
        # optional, so none is okay
        if values.get("sector_code") == None:
            # but just make sure there's no other attributes set
            assert len(values) == 0, "invalid attribute: " + str(values.keys())
            return values

        assert len(values) == 1, "multiple attributes given, expecting just sector_code"
        assert "sector_code" in values, "unknown attribute given in " + str(
            values.keys()
        )
        for x in values.get("sector_code"):
            assert len(x) == 3, (
                "sector_codes must be between 3 and 5 characters long.  Failed on " + x
            )

        return values


class date_filter(BaseModel):
    # inputs
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    period: Optional[str] = None

    # date values that we'll search with
    start: Optional[date] = None
    end: Optional[date] = None
    periodSymbols = ["d", "w", "m", "y"]

    @validator("start_date", "end_date", pre=True)
    def check_date_type(cls, v):
        try:
            datetime.strptime(v, "%Y-%m-%d")
            return v
        except:
            assert False, "dates must be formatted as yyyy-mm-dd"

    @root_validator()
    def check_attributes(cls, values):
        # can't set period and start/end
        if values.get("period") != None:
            # make sure they haven't also set a start or end date
            assert (
                values.get("start_date") == None
            ), "Cannot specify 'period' and 'start_date'"
            assert (
                values.get("end_date") == None
            ), "Cannot specify 'period' and 'end_date'"

            assert (
                len(values.get("period")) > 1
            ), "Must specify an integer and a period symbol.  Examples: 1d, 4w, 7y"
            periodSymbol = values.get("period")[-1]
            assert periodSymbol in values.get("periodSymbols"), (
                "Unrecognised period symbol '" + periodSymbol + "'"
            )
        else:
            # can't set end to be before start
            # don't need to worry about typing for start_date or end_date since its validated already
            if values.get("start_date") != None and values.get("end_date") != None:
                start = datetime.strptime(values.get("start_date"), "%Y-%m-%d")
                end = datetime.strptime(values.get("end_date"), "%Y-%m-%d")
                assert start < end, "Cannot specify 'end_date' before 'start_date'"
        return values

    def processSearchDates(self):
        # they didn't give any input at all
        if self.period == None and self.start_date == None and self.end_date == None:
            # search without a date range
            # this technically should never run, given the driver has to check for this anyway when issuing the query
            return True
        elif self.period != None:
            # use period
            return self.setPeriod()
        elif self.start_date == None and self.end_date != None:
            # no start, but end specified. go from the beginning of records
            self.start = datetime.strptime("2001-01-01", "%Y-%m-%d")
            self.end = self.end_date
            return True
        elif self.start_date != None and self.end_date == None:
            # specified start, but no end. go from start until today
            self.start = datetime.strptime(self.start_date, "%Y-%m-%d")
            self.end = date.today()
            return True
        elif self.start_date != None and self.end_date != None:
            # specified a start and an end date
            self.start = datetime.strptime(self.start_date, "%Y-%m-%d")
            self.end = datetime.strptime(self.end_date, "%Y-%m-%d")
            return True
        else:
            # logically this can't happen.... famous last words
            return False

    def setPeriod(self):
        # try catches any issues with date and relativedelta
        try:
            self.end = date.today()
            if self.period[-1] == "d":
                self.start = date.today() + relativedelta(days=-int(self.period[:-1]))
            elif self.period[-1] == "w":
                self.start = date.today() + relativedelta(weeks=-int(self.period[:-1]))
            elif self.period[-1] == "m":
                self.start = date.today() + relativedelta(months=-int(self.period[:-1]))
            elif self.period[-1] == "y":
                self.start = date.today() + relativedelta(years=-int(self.period[:-1]))
            else:
                # default to days
                self.start = date.today() + relativedelta(days=-int(self.period[:-1]))
            return True
        except:
            return False
