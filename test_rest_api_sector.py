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

# SECTOR USE CASE 1
@pytest.mark.parametrize(
    "route, parameter, http_response",
    [
        # noparm
        ("/sector", None, 200),
        # 1parm
        ("/sector", {"sector_code": ["xij"]}, 200),
        # 2parm
        ("/sector", {"sector_code": ["xhj", "xmj"]}, 200),
        # 1longparm
        ("/sector", {"sector_code": ["long code"]}, 422),
        # 1non-existentparm
        # todo: handle invalid sector_codes better - maybe have a key at the end of the return showing ignored/invalid sector_codes?
        # maybe HTTP 207?
        ("/sector", {"sector_code": ["zzz"]}, 200),
        # bad key
        ("/sector", {"fake_key": ["zzz"]}, 422),
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
def test_sector_uc1(route, parameter, http_response):
    do_test(route, parameter, http_response)


# SECTOR USE CASE 2
@pytest.mark.parametrize(
    "route, parameter, http_response",
    [
        # goodrequest
        ("/sector/xmj", None, 200),
        # longrequest
        ("/sector/fake_sector", None, 404),
        # non-existentrequest
        ("/sector/zzz", None, 404),
    ],
    ids=["good request", "bad long request", "bad non-existent request"],
)
def test_sector_uc2(route, parameter, http_response):
    do_test(route, parameter, http_response)


# SECTOR USE CASE 3
@pytest.mark.parametrize(
    "route, parameter, http_response",
    [
        # good request
        ("/sector/xdj/quotes/weekly", None, 200),
        # bad route
        ("/sector/xdj/quotes/fakeendpoint", None, 404),
        # bad request
        ("/sector/fake_sector/quotes/weekly", None, 404),
        # non-existent request
        ("/sector/zzz/quotes/weekly", None, 404),
        # good start date
        ("/sector/xdj/quotes/weekly", {"start_date": "2021-01-01"}, 200),
        # good end date
        ("/sector/xdj/quotes/weekly", {"end_date": "2021-01-01"}, 200),
        # bad start date
        ("/sector/xdj/quotes/weekly", {"start_date": "abc"}, 422),
        # bad end date
        ("/sector/xdj/quotes/weekly", {"end_date": "abc"}, 422),
        # good start and end dates
        (
            "/sector/xdj/quotes/weekly",
            {"start_date": "2021-01-01", "end_date": "2021-02-01"},
            200,
        ),
        # bad end before start date
        (
            "/sector/xdj/quotes/weekly",
            {"start_date": "2022-12-31", "end_date": "2021-01-01"},
            422,
        ),
        # good period days
        ("/sector/xdj/quotes/weekly", {"period": "100d"}, 200),
        # good period weeks
        ("/sector/xdj/quotes/weekly", {"period": "10w"}, 200),
        # good period months
        ("/sector/xdj/quotes/weekly", {"period": "3m"}, 200),
        # good period years
        ("/sector/xdj/quotes/weekly", {"period": "1y"}, 200),
        # bad period blank
        ("/sector/xdj/quotes/weekly", {"period": ""}, 422),  # invalid period
        # good period None
        ("/sector/xdj/quotes/weekly", {"period": None}, 400),  # invalid period
        # bad key
        ("/sector/xdj/quotes/weekly", {"fake_parameter": None}, 400),  # invalid request
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
def test_sector_uc3(route, parameter, http_response):
    do_test(route, parameter, http_response)


# SECTOR USE CASE 4
@pytest.mark.parametrize(
    "route, parameter, http_response",
    [
        # good sector good date
        ("/sector/xdj/quotes/weekly/2021-06-06", None, 200),
        # bad sector good date
        ("/sector/zzz/quotes/weekly/2021-06-06", None, 404),
        # good sector bad date
        ("/sector/xdj/quotes/weekly/2021-07-02", None, 404),
    ],
    ids=[
        "good sector good date",
        "bad sector good date",
        "good sector bad date",
    ],
)
def test_sector_uc4(route, parameter, http_response):
    do_test(route, parameter, http_response)


# SECTOR USE CASE 5
@pytest.mark.parametrize(
    "route, parameter, http_response",
    [
        # good no parm
        ("/quote/sector/weekly", None, 200),
        # good 1 parm
        ("/quote/sector/weekly", {"sector_code": ["xdj"]}, 200),  # one valid code
        # good 2 parm
        (
            "/quote/sector/weekly",
            {"sector_code": ["xdj", "xmj"]},
            200,
        ),
        # good 1 non-existent parm, 1 good parm
        (
            "/quote/sector/weekly",
            {"sector_code": ["zzz", "xmj"]},
            200,
        ),
        # good 1 long parm, 1 good parm
        (
            "/quote/sector/weekly",
            {"sector_code": ["code too long", "xmj"]},
            422,
        ),
        # bad 1 parm wrong Type
        (
            "/quote/sector/weekly",
            {"sector_code": "bad_type"},
            422,
        ),
        # bad 1 parm None
        (
            "/quote/sector/weekly",
            {"sector_code": None},
            422,
        ),
        # bad key
        ("/quote/sector/weekly", {"fake_parameter": None}, 422),  # invalid request
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
def test_sector_uc5(route, parameter, http_response):
    do_test(route, parameter, http_response)


# SECTOR USE CASE 6
@pytest.mark.parametrize(
    "route, parameter, http_response",
    [
        # good no parm
        ("/quote/sector/weekly/2021-06-06", None, 200),
        # good 1 parm
        (
            "/quote/sector/weekly/2021-06-06",
            {"sector_code": ["xmj"]},
            200,
        ),
        # good 2 parm
        (
            "/quote/sector/weekly/2021-06-06",
            {"sector_code": ["xmj", "xhj"]},
            200,
        ),
        # bad 1 long parm 1 good parm
        (
            "/quote/sector/weekly/2021-06-06",
            {"sector_code": ["one bad parameter", "xhj"]},
            422,
        ),
        # bad invalid quote date
        ("/quote/sector/weekly/2021-06-05", None, 404),  # no weekly data for this date
        # bad 1 parm wrong Type
        (
            "/quote/sector/weekly/2021-06-06",
            {"sector_code": "bad type"},
            422,
        ),  # bad type
        # good non-existent parm
        # todo: should give a 207 or something
        ("/quote/sector/weekly/2021-06-06", {"sector_code": ["zzz"]}, 404),  # fake code
        # bad 1 parm None
        (
            "/quote/sector/weekly/2021-06-06",
            {"sector_code": None},
            422,
        ),
        # bad long request
        (
            "/quote/sector/weekly/2021-06-06",
            {"sector_code": ["code too long"]},
            422,
        ),
        # bad request
        (
            "/quote/sector/weekly/2021-06-06",
            {"fake_parameter": ["xhj"]},
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
def test_sector_uc6(route, parameter, http_response):
    do_test(route, parameter, http_response)


def do_test(route, parameter, http_response):
    response = requests.get(rest_endpoint + route, json=parameter)
    if not response.status_code == http_response:
        pass
    assert response.status_code == http_response
