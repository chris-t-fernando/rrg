import requests
import json
import logging, sys

# from fastapi.testclient import TestClient
# from rest_api.driver_main import app
import pytest
import boto3

logging.basicConfig(stream=sys.stderr, level=logging.INFO)

# client = TestClient(app)

ssm = boto3.client("ssm")
rest_endpoint = (
    ssm.get_parameter(Name="/rrg-creator/rest-endpoint").get("Parameter").get("Value")
)

# STOCK USE CASE 1
@pytest.mark.parametrize(
    "route, parameter, http_response",
    [
        # noparm
        ("/stock", None, 200),
        # 1parm
        ("/stock", {"stock_code": ["z1p"]}, 200),
        # 2parm
        ("/stock", {"stock_code": ["avh", "bhp"]}, 200),
        # 1longparm
        ("/stock", {"stock_code": ["long code"]}, 422),
        # 1non-existentparm
        # todo: handle invalid stock_codes better - maybe have a key at the end of the return showing ignored/invalid stock_codes?
        # maybe HTTP 207?
        ("/stock", {"stock_code": ["zzz"]}, 200),
        # bad key
        ("/stock", {"fake_key": ["zzz"]}, 422),
    ],
    ids=[
        "good no parm",
        "good 1 parm",
        "good 2 parm",
        "bad 1 long parm",
        "good 1 non-existent parm",
        "bad key",
    ],
)
def test_stock_uc1(route, parameter, http_response):
    do_test(route, parameter, http_response)


# STOCK USE CASE 2
@pytest.mark.parametrize(
    "route, parameter, http_response",
    [
        # goodrequest
        ("/stock/bhp", None, 200),
        # longrequest
        ("/stock/fake_stock", None, 404),
        # non-existentrequest
        ("/stock/zzz", None, 404),
    ],
    ids=["good request", "bad long request", "bad non-existent request"],
)
def test_stock_uc2(route, parameter, http_response):
    do_test(route, parameter, http_response)


# STOCK USE CASE 3
@pytest.mark.parametrize(
    "route, parameter, http_response",
    [
        # good request
        ("/stock/14d/quotes/weekly", None, 200),
        # bad route
        ("/stock/14d/quotes/fakeendpoint", None, 404),
        # bad request
        ("/stock/fake_stock/quotes/weekly", None, 404),
        # non-existent request
        ("/stock/zzz/quotes/weekly", None, 404),
        # good start date
        ("/stock/14d/quotes/weekly", {"start_date": "2021-01-01"}, 200),
        # good end date
        ("/stock/14d/quotes/weekly", {"end_date": "2021-01-01"}, 200),
        # bad start date
        ("/stock/14d/quotes/weekly", {"start_date": "abc"}, 422),
        # bad end date
        ("/stock/14d/quotes/weekly", {"end_date": "abc"}, 422),
        # good start and end dates
        (
            "/stock/14d/quotes/weekly",
            {"start_date": "2021-01-01", "end_date": "2021-02-01"},
            200,
        ),
        # bad end before start date
        (
            "/stock/14d/quotes/weekly",
            {"start_date": "2022-12-31", "end_date": "2021-01-01"},
            422,
        ),
        # good period days
        ("/stock/14d/quotes/weekly", {"period": "100d"}, 200),
        # good period weeks
        ("/stock/14d/quotes/weekly", {"period": "10w"}, 200),
        # good period months
        ("/stock/14d/quotes/weekly", {"period": "3m"}, 200),
        # good period years
        ("/stock/14d/quotes/weekly", {"period": "1y"}, 200),
        # bad period blank
        ("/stock/14d/quotes/weekly", {"period": ""}, 422),  # invalid period
        # good period None
        ("/stock/14d/quotes/weekly", {"period": None}, 400),  # invalid period
        # bad key
        ("/stock/14d/quotes/weekly", {"fake_parameter": None}, 400),  # invalid request
    ],
    ids=[
        "good request",
        "bad route",
        "bad request",
        "non-existent request",
        "good start date",
        "good end date",
        "bad start date",
        "bad end date",
        "good start and end dates",
        "bad end before start date",
        "good period days",
        "good period weeks",
        "good period months",
        "good period years",
        "bad period blank",
        "bad period None",
        "bad key",
    ],
)
def test_stock_uc3(route, parameter, http_response):
    do_test(route, parameter, http_response)


# STOCK USE CASE 4
@pytest.mark.parametrize(
    "route, parameter, http_response",
    [
        # good stock good date
        ("/stock/14d/quotes/weekly/2021-07-01", None, 200),
        # bad stock good date
        ("/stock/zzz/quotes/weekly/2021-07-01", None, 404),
        # good stock bad date
        ("/stock/14d/quotes/weekly/2021-07-02", None, 404),
    ],
    ids=[
        "good stock good date",
        "bad stock good date",
        "good stock bad date",
    ],
)
def test_stock_uc4(route, parameter, http_response):
    do_test(route, parameter, http_response)


# STOCK USE CASE 5
@pytest.mark.parametrize(
    "route, parameter, http_response",
    [
        # good no parm
        ("/quote/stock/weekly", None, 200),
        # good 1 parm
        ("/quote/stock/weekly", {"stock_code": ["14d"]}, 200),  # one valid code
        # good 2 parm
        (
            "/quote/stock/weekly",
            {"stock_code": ["14d", "bhp"]},
            200,
        ),
        # good 1 non-existent parm, 1 good parm
        (
            "/quote/stock/weekly",
            {"stock_code": ["zzz", "bhp"]},
            200,
        ),
        # good 1 long parm, 1 good parm
        (
            "/quote/stock/weekly",
            {"stock_code": ["code too long", "bhp"]},
            422,
        ),
        # bad 1 parm wrong Type
        (
            "/quote/stock/weekly",
            {"stock_code": "bad_type"},
            422,
        ),
        # bad 1 parm None
        (
            "/quote/stock/weekly",
            {"stock_code": None},
            422,
        ),
        # bad key
        ("/quote/stock/weekly", {"fake_parameter": None}, 422),  # invalid request
    ],
    ids=[
        "good no parm",
        "good 1 parm",
        "good 2 parms",
        "good 1 non-existent parm, 1 good parm",
        "good 1 long parm, 1 good parm",
        "bad 1 parm wrong Type",
        "bad 1 parm None",
        "bad key",
    ],
)
def test_stock_uc5(route, parameter, http_response):
    do_test(route, parameter, http_response)


# STOCK USE CASE 6
@pytest.mark.parametrize(
    "route, parameter, http_response",
    [
        # good no parm
        ("/quote/stock/weekly/2021-03-15", None, 200),
        # good 1 parm
        (
            "/quote/stock/weekly/2021-03-15",
            {"stock_code": ["bhp"]},
            200,
        ),
        # good 2 parm
        (
            "/quote/stock/weekly/2021-03-15",
            {"stock_code": ["bhp", "avh"]},
            200,
        ),
        # bad 1 long parm 1 good parm
        (
            "/quote/stock/weekly/2021-03-15",
            {"stock_code": ["one bad parameter", "avh"]},
            422,
        ),
        # bad invalid quote date
        ("/quote/stock/weekly/2021-03-14", None, 404),  # no weekly data for this date
        # bad 1 parm wrong Type
        ("/quote/stock/weekly/2021-03-15", {"stock_code": "bad type"}, 422),  # bad type
        # good non-existent parm
        # todo: should give a 207 or something
        ("/quote/stock/weekly/2021-03-15", {"stock_code": ["zzz"]}, 404),  # fake code
        # bad 1 parm None
        (
            "/quote/stock/weekly/2021-03-15",
            {"stock_code": None},
            422,
        ),
        # bad long request
        (
            "/quote/stock/weekly/2021-03-15",
            {"stock_code": ["code too long"]},
            422,
        ),
        # bad request
        (
            "/quote/stock/weekly/2021-03-15",
            {"fake_parameter": ["avh"]},
            422,
        ),
    ],
    ids=[
        "good no parm",
        "good 1 parm",
        "good 2 parms",
        "bad 1 long 1 good",
        "bad invalid quote date",
        "bad 1 parm wrong Type",
        "good non-existent parm",
        "bad 1 parm None",
        "bad long request",
        "bad request",
    ],
)
def test_stock_uc6(route, parameter, http_response):
    do_test(route, parameter, http_response)


def do_test(route, parameter, http_response):
    response = requests.get(rest_endpoint + route, json=parameter)
    if not response.status_code == http_response:
        pass
    assert response.status_code == http_response
